from PIL import Image
import numpy as np
from celery import shared_task


@shared_task
def run(original_dataset_id):
    original_dataset = Dataset.objects.get(id=original_dataset_id)
    with open(original_dataset.content) as input_image:
        average_color = [int(value) for value in np.average(input_image, axis=(0, 1))]
        output_image = Image.new(mode="RGBA", size=(200, 200), color=tuple(average_color))
        return {
            'color_rgba': average_color,
            'color_square': output_image,
        }
