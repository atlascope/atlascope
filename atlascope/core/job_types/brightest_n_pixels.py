from PIL import Image
import numpy as np
from celery import shared_task


@shared_task
def run(original_dataset_id, n):
    original_dataset = Dataset.objects.get(id=original_dataset_id)
    with open(original_dataset.content) as input_image:
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

        return {
            'pixel_locations': brightest,
            'circled_locations': output_image,
        }
