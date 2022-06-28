"""Detect likely locations of nuclei in the image."""
import io

from celery import shared_task
from django.contrib.gis.geos import Point, Polygon
import histomicstk as htk
import numpy as np
import scipy as sp
import skimage.color
import skimage.io
import skimage.measure

from atlascope.core.models import Dataset, DetectedNucleus
from atlascope.core.models.detected_nucleus import (
    NUCLEUS_ATTRIBUTES,
    nucleus_attribute_to_field_name,
)

from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


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

    return additional_features.to_dict("records")


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
                nucleus_attribute_to_field_name(attribute): nucleus[attribute]
                for attribute in NUCLEUS_ATTRIBUTES
            }
            DetectedNucleus.objects.create(
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
