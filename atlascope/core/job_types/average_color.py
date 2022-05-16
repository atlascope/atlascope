"""Return the average among all RGBA values in the input dataset image."""

import io

from PIL import Image
from celery import shared_task
import numpy as np

from atlascope.core.models import Dataset

from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


@shared_task
def run(job_id: str, original_dataset_id: str):
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    input_image = Image.open(io.BytesIO(original_dataset.content.read())).convert("RGB")

    average_color = [int(value) for value in np.average(input_image, axis=(0, 1))]
    output_image = Image.new(mode="RGBA", size=(200, 200), color=tuple(average_color))

    job.resulting_datasets.add(
        save_output_dataset(
            original_dataset,
            job.investigation,
            'Average Color',
            output_image,
            {'rgba': average_color},
        )
    )
    job.complete = True
    job.save()
