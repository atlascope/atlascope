import io
import numpy as np
from PIL import Image
from celery import shared_task
from django.utils import timezone
from atlascope.core.models import Dataset

from .utils import PIL_to_image_file


@shared_task
def run(original_dataset_id):
    original_dataset = Dataset.objects.get(id=original_dataset_id)
    # TODO: we need a module to parse dataset type and return an image from it
    #   This is currently only tolerant to Green Cell Image dataset,
    #   which has PNG content
    input_image = Image.open(io.BytesIO(original_dataset.content.read()))

    average_color = [int(value) for value in np.average(input_image, axis=(0, 1))]
    output_image = Image.new(mode="RGBA", size=(200, 200), color=tuple(average_color))

    new_dataset = Dataset(
        name=f'{original_dataset.name} Average Color',
        description=f'Average color of {original_dataset.name} as of {timezone.now()}',
        public=original_dataset.public,
        metadata={'origin': f'Job Spawned at {timezone.now()}', 'rgba': average_color},
        dataset_type='analytics',
        source_dataset=original_dataset,
    )
    new_dataset.content.save(
        'average_color.png',
        PIL_to_image_file(output_image),
    )
    new_dataset.save()
