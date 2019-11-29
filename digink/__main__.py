#!/bin/env python
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps  # type: ignore
from typing import NamedTuple

from .screens import get_screens
from .images import get_image


if __name__ == "__main__":
    img_path = get_image()
    img = Image.open(img_path)

    screen_collection = get_screens()

    overall_size = screen_collection.get_overall_size()

    # Restretch the image
    img = ImageOps.fit(img, overall_size)

    # Display the image on every screen
    for screen in screen_collection.screens:
        screen.draw_image(img)
