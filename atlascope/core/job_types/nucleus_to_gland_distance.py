"""Return the average distance from nucleus centroid to nearest gland centroid."""

import io
import math

import PIL
from celery import shared_task
import cv2
import numpy as np
import skimage.io

from atlascope.core.models import Dataset

from .nucleus_detection import detect_nuclei
from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


def generate_gland_map(input_image):
    # https://stackoverflow.com/questions/71865493/is-it-possible-to-create-a-random-shape-on-an-image-in-python
    img = np.zeros((input_image.shape[0], input_image.shape[1], 3)).astype(np.uint8)
    rng = np.random.default_rng()
    noise = rng.integers(0, 255, input_image.shape[:2], np.uint8, True)
    blur = cv2.GaussianBlur(noise, (0, 0), sigmaX=15, sigmaY=15, borderType=cv2.BORDER_DEFAULT)
    stretch = skimage.exposure.rescale_intensity(blur, in_range="image", out_range=(0, 255)).astype(
        np.uint8
    )
    thresh = cv2.threshold(stretch, 175, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.merge([mask, mask, mask])
    result_rgb = cv2.add(img, mask)
    return np.mean(result_rgb, axis=2).astype(np.uint8)


def get_result_image(input_image, nucleus_mask, gland_mask, distances_mask):
    mask_shape = (input_image.shape[1], input_image.shape[0])
    nucleus_mask_color = PIL.Image.new("RGBA", mask_shape, "#0ead38")
    gland_mask_color = PIL.Image.new("RGBA", mask_shape, "#c21d1d")
    distances_mask_color = PIL.Image.new("RGBA", mask_shape, "#ebe72d")

    original = PIL.Image.fromarray(input_image, mode="L").convert("RGBA")
    mask_1 = PIL.Image.fromarray(nucleus_mask, mode="L")
    mask_2 = PIL.Image.fromarray(gland_mask, mode="L")
    distances_mask = distances_mask.convert("L")
    composite = PIL.Image.composite(nucleus_mask_color, original, mask_1)
    composite = PIL.Image.composite(gland_mask_color, composite, mask_2)
    composite = PIL.Image.composite(distances_mask_color, composite, distances_mask)
    return composite


@shared_task
def run(job_id: str, original_dataset_id: str):
    # suppress warnings from high numbers and NaNs in computations
    # we only need this when we are using a randomly generated gland map
    import warnings

    from atlascope.core.models import Job

    # TODO: remove this warning suppression
    warnings.filterwarnings("ignore")

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    try:
        # We cannot use previous nucleus detection results because we do not
        # save the nucleus mask to the database
        # (we need the nucleus mask for the output image)
        input_image = skimage.io.imread(
            io.BytesIO(original_dataset.content.read()),
        )
        nucleus_detections, nucleus_mask = detect_nuclei(input_image)
        nucleus_centroids = [
            (nucleus["Identifier.CentroidX"], nucleus["Identifier.CentroidY"])
            for nucleus in nucleus_detections
        ]

        gland_map = generate_gland_map(input_image)
        gland_detections, gland_mask = detect_nuclei(gland_map)
        gland_centroids = [
            (gland["Identifier.CentroidX"], gland["Identifier.CentroidY"])
            for gland in gland_detections
        ]

        distances = []
        mask_shape = (input_image.shape[1], input_image.shape[0])
        distances_mask = PIL.Image.new("RGB", mask_shape)
        distances_mask_draw = PIL.ImageDraw.Draw(distances_mask)
        for nucleus_centroid in nucleus_centroids:
            minimum = None
            closest = None
            for gland_centroid in gland_centroids:
                distance = math.dist(nucleus_centroid, gland_centroid)
                if not minimum or distance < minimum:
                    minimum = distance
                    closest = gland_centroid
            distances.append(minimum)
            distances_mask_draw.line([nucleus_centroid, closest], width=1)
        average_distance_to_nearest_gland = sum(distances) / len(distances)
        output_image = get_result_image(input_image, nucleus_mask, gland_mask, distances_mask)

        job.resulting_datasets.add(
            save_output_dataset(
                original_dataset,
                job.investigation,
                'Average Nucleus to Nearest Gland Distance',
                output_image,
                {'average_distance_in_pixels': average_distance_to_nearest_gland},
            )
        )
        job.complete = True
    except Exception as e:
        print('FAILURE!')
        print(e)
        job.failure = str(e)
    finally:
        job.save()
