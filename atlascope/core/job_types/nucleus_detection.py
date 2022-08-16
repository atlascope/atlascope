"""Detect likely locations of nuclei in the image."""
import io
import math
from typing import TypedDict

from celery import shared_task
from django.contrib.gis.geos import Point, Polygon
import histomicstk as htk
import numpy as np
import numpy.typing as npt
import scipy as sp
import skimage
import skimage.color
import skimage.io
import skimage.measure

from atlascope.core.fields import Cube
from atlascope.core.models import Dataset, DetectedStructure
from atlascope.core.models.detected_structure import (
    STRUCTURE_ATTRIBUTES,
    structure_attribute_to_field_name,
)

from .utils import save_output_dataset

NucleusFeatures = TypedDict(
    'NucleusFeatures',
    {
        'Identifier.Label': int,
        'Identifier.Xmin': float,
        'Identifier.Ymin': float,
        'Identifier.Xmax': float,
        'Identifier.Ymax': float,
        'Orientation.Orientation': float,
        'Identifier.CentroidX': float,
        'Identifier.CentroidY': float,
    },
)

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


def fingerprint(
    img: npt.NDArray[np.uint],
    img_label: npt.NDArray[np.int_],
    features: NucleusFeatures,
) -> Cube:
    """Get the fingerprint for a nucleus.

    The fingerprint is like a perceptual hash of the nucleus image [1]. The images
    are first resized to 10x10 image and then converted to their SSIM [2]
    representation. The fingerprint is the resized 10x10 image. Given a consistent
    ordering of the 10x10 2D array to a 100-dimensional vector, the fingerprint can
    be thought of as a unit vector in the 100-dimensional space. Two fingerprints
    close (Euclidean distance) in the 100-dimensional space are "structurally similar".

    [1] https://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html
    [2] https://en.wikipedia.org/wiki/Structural_similarity
    """
    label = int(features['Label'])
    y_min = int(features['Identifier.Ymin'])
    y_max = int(features['Identifier.Ymax'])
    x_min = int(features['Identifier.Xmin'])
    x_max = int(features['Identifier.Xmax'])
    centroid_x = features['Identifier.CentroidX'] - x_min
    centroid_y = features['Identifier.CentroidY'] - y_min
    orientation = features['Orientation.Orientation']

    # Extract image
    extracted_img = img[y_min:y_max, x_min:x_max]
    extracted_mask = img_label[y_min:y_max, x_min:x_max] == label

    # Rotate the image
    rotated_img = skimage.transform.rotate(
        extracted_img,
        -math.degrees(orientation),
        center=(centroid_y, centroid_x),
        resize=True,
    )
    rotated_mask = skimage.transform.rotate(
        extracted_mask,
        -math.degrees(orientation),
        center=(centroid_y, centroid_x),
        resize=True,
    )

    # Crop rotated image to remove extra padding
    rotated_y_width, rotated_x_width = rotated_mask.shape
    crop_x_begin = 0
    while not np.any(rotated_mask[:, crop_x_begin]):
        crop_x_begin += 1
    crop_x_end = rotated_x_width
    while not np.any(rotated_mask[:, crop_x_end - 1]):
        crop_x_end -= 1
    crop_y_begin = 0
    while not np.any(rotated_mask[crop_y_begin, :]):
        crop_y_begin += 1
    crop_y_end = rotated_y_width
    while not np.any(rotated_mask[crop_y_end - 1, :]):
        crop_y_end -= 1
    cropped_img = rotated_img[crop_y_begin:crop_y_end, crop_x_begin:crop_x_end]
    cropped_mask = rotated_mask[crop_y_begin:crop_y_end, crop_x_begin:crop_x_end]

    # Pad image to be a square
    cropped_len = max(cropped_img.shape)
    pad_x = cropped_len - cropped_img.shape[1]
    pad_y = cropped_len - cropped_img.shape[0]
    padded_img = np.pad(cropped_img, ((0, pad_y), (0, pad_x)))
    padded_mask = np.pad(cropped_mask, ((0, pad_y), (0, pad_x)))

    # Fill null space with mean of image
    masked_img_array = np.ma.masked_array(
        padded_img,
        mask=(padded_mask == False),  # noqa: E712
    )
    mean = masked_img_array.mean()
    mean_filled_img = masked_img_array.filled(fill_value=mean)

    # Resize to 10x10
    resized_img = skimage.transform.resize_local_mean(
        mean_filled_img,
        (10, 10),
        grid_mode=False,
    )

    # Compute SSIM
    fingerprint = (resized_img - mean) / resized_img.std()

    return Cube(fingerprint.flatten())


def detect_nuclei(input_image):
    # Invert image
    input_image = skimage.util.invert(input_image)

    # segment foreground
    foreground_threshold = 150
    im_fgnd_mask = sp.ndimage.binary_fill_holes(input_image < foreground_threshold)

    # run adaptive multi-scale LoG filter
    min_radius = 5
    max_radius = 15

    im_log_max, im_sigma_max = htk.filters.shape.cdog(
        input_image,
        im_fgnd_mask,
        sigma_min=min_radius * np.sqrt(2),
        sigma_max=max_radius * np.sqrt(2),
    )

    # detect and segment nuclei using local maximum clustering
    local_max_search_radius = 5

    im_nuclei_seg_mask, seeds, maxima = htk.segmentation.nuclear.max_clustering(
        im_log_max, im_fgnd_mask, local_max_search_radius
    )

    # filter out small objects
    min_nucleus_area = 80

    im_nuclei_seg_mask = htk.segmentation.label.area_open(
        im_nuclei_seg_mask, min_nucleus_area
    ).astype(int)

    additional_features = htk.features.compute_nuclei_features(
        im_nuclei_seg_mask,
        input_image,
    )

    additional_features_dicts = additional_features.to_dict("records")
    for feature_dict in additional_features_dicts:
        feature_dict["Fingerprint"] = fingerprint(input_image, im_nuclei_seg_mask, feature_dict)
    return additional_features_dicts


@shared_task
def run(job_id: str, original_dataset_id: str):
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    def nucleus_data_subset(data: dict, subset_name: str):
        return (
            {
                key.replace(subset_name, ''): value
                for key, value in data.items()
                if subset_name in key
            },
        )

    try:
        input_image = skimage.io.imread(
            io.BytesIO(original_dataset.content.read()),
        )
        nuclei = detect_nuclei(input_image)

        detection_dataset = save_output_dataset(
            original_dataset,
            job.investigation,
            'Detected Nuclei',
            None,
            {
                'num_nuclei': len(nuclei),
            },
            dataset_type='nucleus_detection',
        )
        for nucleus in nuclei:
            additional_nucleus_attributes = {
                structure_attribute_to_field_name(attribute): nucleus[attribute]
                for attribute in STRUCTURE_ATTRIBUTES
            }
            DetectedStructure.objects.create(
                detection_dataset=detection_dataset,
                label_integer=nucleus['Label'],
                centroid=Point(
                    x=nucleus['Identifier.CentroidX'],
                    y=nucleus['Identifier.CentroidY'],
                ),
                weighted_centroid=Point(
                    x=nucleus['Identifier.WeightedCentroidX'],
                    y=nucleus['Identifier.WeightedCentroidY'],
                ),
                bounding_box=Polygon(
                    [
                        (nucleus['Identifier.Xmin'], nucleus['Identifier.Ymin']),
                        (nucleus['Identifier.Xmax'], nucleus['Identifier.Ymin']),
                        (nucleus['Identifier.Xmax'], nucleus['Identifier.Ymax']),
                        (nucleus['Identifier.Xmin'], nucleus['Identifier.Ymax']),
                        # repeat first point to create linear ring
                        (nucleus['Identifier.Xmin'], nucleus['Identifier.Ymin']),
                    ]
                ),
                fingerprint=nucleus['Fingerprint'],
                **additional_nucleus_attributes,
            )

        job.resulting_datasets.add(detection_dataset)
        job.complete = True
        job.save()
    except Exception as e:
        print('FAILURE!')
        print(e)
        job.failure = str(e)
        job.save()
