import os
import random

from PIL import Image
from utils import logx

log = logx.get_logger('some_main')

ORIGINAL_IMAGE_FILE = 'media/parliament.original.png'
DIR_RECOLORED_IMAGES = 'media/parliament.recolored'
FLAG_COLORS = [
    (255, 190, 41),
    (141, 21, 58),
    (235, 116, 0),
    (0, 83, 78),
]


def main():
    im = Image.open(ORIGINAL_IMAGE_FILE)
    width, height = im.size

    pixels = im.load()

    for x in range(width):
        for y in range(height):
            (r, g, b, a) = pixels[x, y]

            if ((r + g + b) / 3 < 224):
                (r, g, b) = random.choice(FLAG_COLORS)
            else:
                (r, g, b, a) = (255, 255, 255, 0)

            pixels[x, y] = (r, g, b, a)

    im.save(os.path.join(DIR_RECOLORED_IMAGES, 'master.png'))

    for file_only, dim in [
        ['favicon.ico', 70],
        ['logo192.png', 192],
        ['logo512.png', 512],
    ]:
        im.resize(
            (dim, dim)).save(
            os.path.join(
                DIR_RECOLORED_IMAGES, file_only))


if __name__ == '__main__':
    main()
