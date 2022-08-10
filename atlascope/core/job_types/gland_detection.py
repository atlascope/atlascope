"""Detect likely locations of glands in the image."""
import io

from celery import shared_task
from django.contrib.gis.geos import Point, Polygon
import skimage.color
import skimage.io
import skimage.measure

from atlascope.core.models import Dataset, DetectedStructure
from atlascope.core.models.detected_structure import (
    STRUCTURE_ATTRIBUTES,
    structure_attribute_to_field_name,
)

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
def run(
    job_id: str,
    original_dataset_id: str,
    gland_map_path=schema["properties"]["gland_map_path"]["default"],
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
        input_image = skimage.io.imread(io.BytesIO(open(gland_map_path, 'rb').read()))
        glands = detect_nuclei(input_image)

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
            # For small sample image, increase the coordinates of the
            # centroids to better match the size of the image
            centroid = Point(
                x=gland['Identifier.CentroidX'] * 3,
                y=gland['Identifier.CentroidY'] * 2.5,
            )
            DetectedStructure.objects.create(
                detection_dataset=detection_dataset,
                structure_type='gland',
                label_integer=gland['Label'],
                centroid=centroid,
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
