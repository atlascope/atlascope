"""Detect likely locations of nuclei in the image."""
import io

# import histomicstk as htk

# import numpy as np
# import scipy as sp

import skimage.io
import skimage.measure
import skimage.color

# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
from celery import shared_task

from atlascope.core.models import Dataset

# from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


@shared_task
def run(job_id: str, original_dataset_id: str):
    from atlascope.core.models import Job

    print()
    print()

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    try:
        print('detecting nuclei...')
        input_image = skimage.io.imread(
            io.BytesIO(original_dataset.content.read()),
        )
        print(input_image)

        # output_image = Image.new(mode="RGBA", size=(200, 200), color=tuple(average_color))

        # job.resulting_datasets.add(
        #     save_output_dataset(
        #         original_dataset,
        #         job.investigation,
        #         'Average Color',
        #         output_image,
        #         {'rgba': average_color},
        #     )
        # )
        job.complete = True
        job.save()
    except Exception as e:
        print('FAILURE!')
        print(e)
        job.failure = str(e)
        job.save()

    print()
    print()
