import io

from PIL import Image, ImageDraw
from celery import shared_task
import numpy as np

from atlascope.core.models import Dataset

from .utils import save_output_dataset


@shared_task
def run(job_id: str, original_dataset_id: str, n: int):
    """Return the locations of the N pixels with the greatest RGB values in the input dataset."""
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)
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

    job.resulting_datasets.add(
        save_output_dataset(
            original_dataset,
            job.investigation,
            f'Brightest {n} Pixels',
            output_image,
            {'pixel_locations': brightest},
        )
    )
    job.complete = True
    job.save()
