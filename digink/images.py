#!/bin/env python
import re
from os import listdir
import os.path
import random

def get_image():
    abspath = os.path.abspath(__file__)
    dname = os.path.join(os.path.dirname(abspath), 'images')
    image_files = [os.path.join(dname, f) for f in listdir(dname) if os.path.isfile(os.path.join(dname, f)) and re.search(r'\.png$', f)]
    img_path = random.choice(image_files)
    return img_path
