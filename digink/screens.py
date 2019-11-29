#!/bin/env python

from __future__ import annotations

from typing import NamedTuple, List, Tuple
from IT8951.display import AutoEPDDisplay  # type: ignore
from IT8951 import constants  # type: ignore
from PIL import Image, ImageDraw, ImageFont, ImageOps  # type: ignore


class Dimensions(NamedTuple):
    start_x: int
    start_y: int
    width: int
    height: int

    def mul(self, amount: float) -> Dimensions:
        return Dimensions(
            start_x=int(self.start_x * amount),
            start_y=int(self.start_y * amount),
            width=int(self.width * amount),
            height=int(self.height * amount),
        )


class Screen(NamedTuple):
    display: AutoEPDDisplay
    physical_dimensions: Dimensions

    def draw_image(self, img):
        display = self.display
        display.frame_buf.paste(
            0xFF, box=(0, 0, self.display.width, self.display.height)
        )
        coords = (
            self.start_x,
            self.start_y,
            self.start_x + self.width,
            self.start_y + self.height,
        )
        screen_part = img.crop(coords)
        display.frame_buf.paste(screen_part)
        display.draw_full(constants.DisplayModes.GC16)


class ScreenCollection(NamedTuple):
    screens: List[Screen]

    def get_physical_overall_size(self) -> Tuple[int, int]:
        max_width = max(
            [
                screen.physical_dimensions.width + screen.physical_dimensions.start_x
                for screen in self.screens
            ]
        )
        max_height = max(
            [
                screen.physical_dimensions.height + screen.physical_dimensions.start_y
                for screen in self.screens
            ]
        )
        max_dims = (max_width, max_height)
        return max_dims

    def draw_image(self, img: Image) -> None:

        physical_overall_size = self.get_physical_overall_size()

        # 1. Redo the image ratio to fit the physical ratio
        # https://stackoverflow.com/a/4744625
        ideal_aspect = physical_overall_size[0] / physical_overall_size[1]
        width, height = img.size
        aspect = width / height
        if aspect > ideal_aspect:
            new_width = int(ideal_aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
        else:
            new_height = int(width / ideal_aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)

        img = img.crop(resize)

        # 2. For each screen, choose the right slice of pixels from the main image it should have
        width_ratio = img.size[0] / physical_overall_size[0]
        # Width ratio is ~= height ratio
        pixel_ratio = width_ratio

        for screen in self.screens:
            # Get the pixel-correct dimensions
            pixel_dimensions = screen.physical_dimensions.mul(pixel_ratio)
            # Get the image-slice we want
            coords = (
                pixel_dimensions.start_x,
                pixel_dimensions.start_y,
                pixel_dimensions.start_x + pixel_dimensions.width,
                pixel_dimensions.start_y + pixel_dimensions.height,
            )
            screen_part = img.crop(coords)
            # resize the screen part to match the screen's pixel dimensions
            display = screen.display
            screen_part = screen_part.resize((display.width, display.height))
            display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
            display.frame_buf.paste(screen_part)
            display.draw_full(constants.DisplayModes.GC16)


def get_screens() -> ScreenCollection:
    screens = [
        Screen(
            physical_dimensions=Dimensions(start_x=0, start_y=0, width=12, height=9,),
            display=AutoEPDDisplay(vcom=-2.06),
        )
    ]
    return ScreenCollection(screens)


# Show on screen(s)

# TODO modify IT class to allow custom pins, so we can drive more than one
# Current pins:
#     CS    = 8
#    HRDY  = 24
#    RESET = 17
# SPI 0:
# https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi
