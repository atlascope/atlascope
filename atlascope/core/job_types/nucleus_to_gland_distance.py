"""Return the average distance from nucleus centroid to nearest gland centroid."""

import math

from celery import shared_task

from atlascope.core.models import Dataset

from .gland_detection import run as run_detect_glands
from .nucleus_detection import run as run_detect_nuclei
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
        # Else run a new job for that information
        nucleus_detections = Job.objects.filter(
            original_dataset=original_dataset,
            job_type='nucleus_detection',
            complete=True,
        )
        if nucleus_detections.count() > 0:
            resulting_dataset = nucleus_detections[0].resulting_datasets.first()
        else:
            new_job = Job.objects.create(
                investigation=job.investigation,
                job_type='nucleus_detection',
                original_dataset=job.original_dataset,
            )
            # Run synchronously
            run_detect_nuclei(new_job.id, original_dataset_id)
            resulting_dataset = new_job.resulting_datasets.first()
        nucleus_detections = list(resulting_dataset.detected_structures.all())
        nucleus_centroids = [
            (nucleus.centroid.x, nucleus.centroid.y) for nucleus in nucleus_detections
        ]

        # If a previous job has gland detections, use that information
        # Else run a new job for that information
        gland_detections = Job.objects.filter(
            original_dataset=original_dataset,
            job_type='gland_detection',
            complete=True,
        )
        if gland_detections.count() > 0:
            resulting_dataset = gland_detections[0].resulting_datasets.first()
        else:
            new_job = Job.objects.create(
                investigation=job.investigation,
                job_type='gland_detection',
                original_dataset=job.original_dataset,
                additional_inputs={'gland_map_path': gland_map_path},
            )
            # Run synchronously
            run_detect_glands(new_job.id, original_dataset_id)
            resulting_dataset = new_job.resulting_datasets.first()
        gland_detections = list(resulting_dataset.detected_structures.all())
        gland_centroids = [(gland.centroid.x, gland.centroid.y) for gland in gland_detections]

        distances = []
        line_coordinates = []
        for nucleus_centroid in nucleus_centroids:
            minimum = None
            closest = None
            for gland_centroid in gland_centroids:
                distance = math.dist(nucleus_centroid, gland_centroid)
                if not minimum or distance < minimum:
                    minimum = distance
                    closest = gland_centroid
            distances.append(minimum)
            line_coordinates.append([nucleus_centroid, closest])
        average_distance_to_nearest_gland = sum(distances) / len(distances)

        job.resulting_datasets.add(
            save_output_dataset(
                original_dataset,
                job.investigation,
                'Average Nucleus to Nearest Gland Distance',
                None,
                {
                    'average_distance_in_pixels': average_distance_to_nearest_gland,
                    'distance_lines': line_coordinates,
                },
                dataset_type='nucleus_gland_dist',
            )
        )
        job.complete = True
    except Exception as e:
        job.failure = str(e)
    finally:
        job.save()
