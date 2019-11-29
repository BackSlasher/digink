#!/bin/env python
import os
from IT8951.display import AutoEPDDisplay
from PIL import Image, ImageDraw, ImageFont
from IT8951 import constants
from typing import NamedTuple


# types
Display = AutoEPDDisplay
class Screen(NamedTuple):
    start_x: int
    start_y: int
    width: int
    height: int
    display: Display

# code

# Decide what photo to show

# TODO actual work

# Fetch it

# TODO actual work
import re
from os import listdir
from os.path import isfile, join
import random
abspath = os.path.abspath(__file__)
dname = join(os.path.dirname(abspath), 'images')
image_files = [join(dname, f) for f in listdir(dname) if isfile(join(dname, f)) and re.search(r'\.png$', f)]
img_path = random.choice(image_files)

# Rastesize

# TODO actual work

# Show on screen(s)

# TODO modify IT class to allow custom pins, so we can drive more than one
# Current pins:
#     CS    = 8
#    HRDY  = 24
#    RESET = 17
# SPI 0:
# https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi



img = Image.open(img_path)

main_display = AutoEPDDisplay(vcom=-2.06)
screens = [
    Screen(
        start_x=0,
        start_y=0,
        width=main_display.width,
        height=main_display.height,
        display=main_display,
    )
]

# Get the overall size
max_width = max([screen.width + screen.start_x for screen in screens])
max_height = max([screen.height + screen.start_y for screen in screens])

dims = (max_width, max_height)

img.thumbnail(dims)

# TODO should we reinstate that?
# paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display

for screen in screens:
    display = screen.display
    display.frame_buf.paste(0xFF, box=(0, 0, screen.width, screen.height))
    coords = (screen.start_x, screen.start_y, screen.start_x + screen.width, screen.start_y + screen.height)
    screen_part = img.crop(coords)
    display.frame_buf.paste(screen_part)
    display.draw_full(constants.DisplayModes.GC16)
