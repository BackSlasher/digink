#!/bin/env python

from typing import NamedTuple, List, Tuple
from IT8951.display import AutoEPDDisplay  # type: ignore
from IT8951 import constants  # type: ignore


class Screen(NamedTuple):
    start_x: int
    start_y: int
    width: int
    height: int
    display: AutoEPDDisplay

    def draw_image(self, img):
        display = self.display
        display.frame_buf.paste(0xFF, box=(0, 0, self.width, self.height))
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

    def get_overall_size(self) -> Tuple[int, int]:
        max_width = max([screen.width + screen.start_x for screen in self.screens])
        max_height = max([screen.height + screen.start_y for screen in self.screens])
        max_dims = (max_width, max_height)
        return max_dims


def get_screens() -> ScreenCollection:
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
    return ScreenCollection(screens)


# Show on screen(s)

# TODO modify IT class to allow custom pins, so we can drive more than one
# Current pins:
#     CS    = 8
#    HRDY  = 24
#    RESET = 17
# SPI 0:
# https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi
