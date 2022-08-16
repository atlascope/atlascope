"""Detect likely locations of glands in the image."""
import io

from celery import shared_task
from django.contrib.gis.geos import Point, Polygon
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

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}

NUM_GLANDS_TO_GENERATE = 20


def detect_glands(input_image):
    glands = []
    y = input_image.shape[0]
    x = input_image.shape[1]
    for n in range(NUM_GLANDS_TO_GENERATE):
        dx = 5
        dy = int(NUM_GLANDS_TO_GENERATE / dx)
        centroid = [
            ((n % dx) + 1) * (x / (dx + 2)),
            ((n % dy) + 1) * (y / (dy + 2)),
        ]
        gland = {
            'Label': n,
            'Identifier.CentroidX': centroid[0],
            'Identifier.CentroidY': centroid[1],
            'Identifier.WeightedCentroidX': centroid[0],
            'Identifier.WeightedCentroidY': centroid[1],
            'Identifier.Xmin': 0,
            'Identifier.Xmax': 0,
            'Identifier.Ymin': 0,
            'Identifier.Ymax': 0,
        }
        gland.update({attribute: 0 for attribute in STRUCTURE_ATTRIBUTES})
        glands.append(gland)
    return glands


@shared_task
def run(
    job_id: str,
    original_dataset_id: str,
):
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    def gland_data_subset(data: dict, subset_name: str):
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
        glands = detect_glands(input_image)

        detection_dataset = save_output_dataset(
            original_dataset,
            job.investigation,
            'Detected Glands',
            None,
            {
                'num_glands': len(glands),
            },
            dataset_type='gland_detection',
        )
        for gland in glands:
            additional_gland_attributes = {
                structure_attribute_to_field_name(attribute): gland[attribute]
                for attribute in STRUCTURE_ATTRIBUTES
            }
            DetectedStructure.objects.create(
                detection_dataset=detection_dataset,
                structure_type='gland',
                label_integer=gland['Label'],
                centroid=Point(
                    x=gland['Identifier.CentroidX'],
                    y=gland['Identifier.CentroidY'],
                ),
                weighted_centroid=Point(
                    x=gland['Identifier.WeightedCentroidX'],
                    y=gland['Identifier.WeightedCentroidY'],
                ),
                bounding_box=Polygon(
                    [
                        (gland['Identifier.Xmin'], gland['Identifier.Ymin']),
                        (gland['Identifier.Xmax'], gland['Identifier.Ymin']),
                        (gland['Identifier.Xmax'], gland['Identifier.Ymax']),
                        (gland['Identifier.Xmin'], gland['Identifier.Ymax']),
                        # repeat first point to create linear ring
                        (gland['Identifier.Xmin'], gland['Identifier.Ymin']),
                    ]
                ),
                fingerprint=Cube([-9999] * 100),
                **additional_gland_attributes,
            )

        job.resulting_datasets.add(detection_dataset)
        job.complete = True
        job.save()
    except Exception as e:
        print('FAILURE!')
        print(e)
        job.failure = str(e)
        job.save()
