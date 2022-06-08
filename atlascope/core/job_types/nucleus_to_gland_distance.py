"""Return the average distance from nucleus centroid to nearest gland centroid."""

import io
import math

from celery import shared_task
import skimage.io

from atlascope.core.models import Dataset

from .nucleus_detection import detect_nuclei
from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {
        "gland_map_path": {
            "type": 'string',
            "title": 'Path to gland map',
            "default": 'atlascope/core/management/populate/inputs/gland_map.jpg',
        }
    },
}


@shared_task
def run(job_id: str, original_dataset_id: str, gland_map_path: str):
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    try:
        # If a previous job has nucleus detections, use that information
        nucleus_detections = Job.objects.filter(
            original_dataset=original_dataset,
            job_type='nucleus_detection',
        )
        if nucleus_detections.count() > 0:
            nucleus_detections = list(
                nucleus_detections[0].resulting_datasets.first().detected_nuclei.all()
            )
            nucleus_centroids = [
                (nucleus.centroid.x, nucleus.centroid.y) for nucleus in nucleus_detections
            ]
        else:
            input_image = skimage.io.imread(
                io.BytesIO(original_dataset.content.read()),
            )
            nucleus_detections = detect_nuclei(input_image)
            nucleus_centroids = [
                (nucleus["Identifier.CentroidX"], nucleus["Identifier.CentroidY"])
                for nucleus in nucleus_detections
            ]

        gland_map = skimage.io.imread(io.BytesIO(open(gland_map_path, 'rb').read()))
        gland_detections = detect_nuclei(gland_map)
        gland_centroids = [
            (gland["Identifier.CentroidX"], gland["Identifier.CentroidY"])
            for gland in gland_detections
        ]

        distances = [
            min([math.dist(nucleus_centroid, gland_centroid) for gland_centroid in gland_centroids])
            for nucleus_centroid in nucleus_centroids
        ]
        average_distance_to_nearest_gland = sum(distances) / len(distances)

        job.resulting_datasets.add(
            save_output_dataset(
                original_dataset,
                job.investigation,
                'Average Nucleus to Nearest Gland Distance',
                None,
                {'average_distance_in_pixels': average_distance_to_nearest_gland},
            )
        )
        job.complete = True
    except Exception as e:
        job.failure = str(e)
    finally:
        job.save()
