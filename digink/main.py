#!/bin/env python
# CD to script's dir
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Decide what photo to show

# TODO actual work

# Fetch it

# TODO actual work

img_path = "images/2.png"

# Rastesize

# TODO actual work

# Show on screen(s)

# TODO modify IT class to allow custom pins, so we can drive more than one
from IT8951.display import AutoEPDDisplay
from PIL import Image, ImageDraw, ImageFont
from IT8951 import constants

print('Initializing EPD...')
display = AutoEPDDisplay(vcom=-2.06)
print('VCOM set to', display.epd.get_vcom())
display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
img = Image.open(img_path)

dims = (display.width, display.height)

img.thumbnail(dims)
paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
display.frame_buf.paste(img, paste_coords)

display.draw_full(constants.DisplayModes.GC16)

