from PIL import Image
import numpy as np

"""
Main function of image analysis job
- Accepts input image (as a pillow Image) and additional kwargs.
- Should return an array of one or more outputs.
- Any outputs that are pillow Images will be saved as image outputs.
- Any other output types must be JSON serializable.
"""


def main(input_image, **kwargs):
    average_color = tuple([int(value) for value in np.average(input_image, axis=(0, 1))])
    output_image = Image.new(mode="RGBA", size=(200, 200), color=average_color)
    return [output_image]
