from PIL import Image
import numpy as np

"""
Main function of image analysis job
- Accepts input image (as a pillow Image) and additional kwargs.
- Should return a dict of one or more outputs.
- Any outputs that are pillow Images will be saved as image outputs.
- Any other output types must be JSON serializable.
"""


def main(input_image, **kwargs):
    average_color = [int(value) for value in np.average(input_image, axis=(0, 1))]
    output_image = Image.new(mode="RGBA", size=(200, 200), color=tuple(average_color))
    return {
        'color_rgba': average_color,
        'color_square': output_image,
    }
