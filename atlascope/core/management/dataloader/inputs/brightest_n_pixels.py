import numpy as np
from PIL import ImageDraw


'''
Main function of image analysis job
- Accepts input image (as a pillow Image) and additional kwargs.
- Should return an array of one or more outputs.
- Any outputs that are pillow Images will be saved as image outputs.
- Any other output types must be JSON serializable.
'''


def main(input_image, **kwargs):
    output_image = input_image.copy()

    data = np.array(input_image)
    data = np.apply_along_axis(lambda arr: arr[:-1], 2, data)
    data = np.apply_along_axis(np.sum, 2, data)
    data = np.transpose(data)

    brightest = []
    while len(brightest) < kwargs['n']:
        max = np.max(data)
        maxloc = list(zip(*np.where(data == max)))[0]
        surrounding10 = [
            (maxloc[0] - 5 + i, maxloc[1] - 5 + j) for i in range(10) for j in range(10)
        ]
        for pixel in surrounding10:
            data[pixel[0]][pixel[1]] = 0
        brightest.append(maxloc)

    draw = ImageDraw.Draw(output_image)
    for location in brightest:
        bounding_box = (
            location[0] - 5,
            location[1] - 5,
            location[0] + 5,
            location[1] + 5,
        )
        draw.ellipse(bounding_box, outline=(255, 0, 0), width=3)

    return [
        output_image,
        f'Brightest locations = {str(brightest)}',
    ]
