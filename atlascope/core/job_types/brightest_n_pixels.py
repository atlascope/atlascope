import io

from PIL import Image, ImageDraw
from celery import shared_task
from django.utils import timezone
import numpy as np

from atlascope.core.models import Dataset

from .utils import to_saveable_image


@shared_task
def run(original_dataset_id, n):
    """Return the locations of the N pixels with the greatest RGB values in the input dataset."""
    original_dataset = Dataset.objects.get(id=original_dataset_id)
    # TODO: we need a module to parse dataset type and return an image from it
    #   This is currently only tolerant to Green Cell Image dataset,
    #   which has PNG content
    input_image = Image.open(io.BytesIO(original_dataset.content.read()))
    output_image = input_image.copy()

    data = np.array(input_image)
    data = np.apply_along_axis(lambda arr: arr[:-1], 2, data)
    data = np.apply_along_axis(np.sum, 2, data)
    data = np.transpose(data)

    brightest = []
    while len(brightest) < n:
        max = np.max(data)
        maxloc = list(zip(*np.where(data == max)))[0]
        surrounding10 = [
            (maxloc[0] - 5 + i, maxloc[1] - 5 + j) for i in range(10) for j in range(10)
        ]
        for pixel in surrounding10:
            data[pixel[0]][pixel[1]] = 0
        brightest.append([int(val) for val in maxloc])

    draw = ImageDraw.Draw(output_image)
    for location in brightest:
        bounding_box = (
            location[0] - 5,
            location[1] - 5,
            location[0] + 5,
            location[1] + 5,
        )
        draw.ellipse(bounding_box, outline=(255, 0, 0), width=3)

    new_dataset = Dataset(
        name=f'{original_dataset.name} Brightest {n} Pixels',
        description=f'Brightest Pixels in {original_dataset.name} as of {timezone.now()}',
        public=original_dataset.public,
        metadata={'origin': f'Job Spawned at {timezone.now()}', 'pixel_locations': brightest},
        dataset_type='analytics',
        source_dataset=original_dataset,
    )
    new_dataset.content.save(
        f'brightest_{n}_pixels.png',
        to_saveable_image(output_image),
    )
    new_dataset.save()

    original_dataset.derived_datasets.add(new_dataset)
