from enum import Enum
from os import path
from typing import Dict

import numpy as np
from customtkinter import CTkImage
from PIL import Image as Pillow
from PIL.Image import Image


class Icon(Enum):
    """Enumerates all possible icons available."""

    robot = "robot"
    flag = "flag"
    no_entry = "do-not-enter"


class IconLoader(object):
    """Load Icon images into the application."""

    _instance = None

    cache: Dict[Icon, CTkImage] = {}

    def __new__(cls):
        """Create a config object.

        Overridden to provide the singleton patten, there must only be one
        IconLoader object. there should only be one cache so there is not need
        for more than one loader

        Returns:
            IconLoader: The config object with the loaded data
        """
        # https://python-patterns.guide/gang-of-four/singleton/
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_path(self, icon: Icon) -> str:
        """Get an icon's file path.

        Args:
            icon (Icon): the icon to find the path for.

        Returns:
            str: the absolute path to the icon file.
        """
        return path.abspath(
            path.join(path.dirname(__file__), f"{icon.value}.png")
        )

    def get_light_icon(self, image: Image) -> Image:
        """Convert a black icon to a wight one for light and dark themes.

        sets all non-transparent pixels to wight.

        Args:
            image (Image): the image to convert,

        Returns:
            Image: the image with a white foreground
        """
        img_array = np.array(image)

        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        non_transparent_pixels = alpha != 0
        # set icon color to wight
        rgb[non_transparent_pixels] = [255, 255, 255]

        return Pillow.fromarray(img_array)

    def get_icon(self, icon: Icon) -> CTkImage:
        """Get the custom tkinter image object for a given icon.

        Args:
            icon (Icon): the icon to display

        Returns:
            CTkImage: the image representing this icon in light and dark themes
        """
        existing_image = self.cache.get(icon, None)
        if existing_image is not None:
            return existing_image

        icon_image_raw = Pillow.open(self.get_path(icon))

        self.cache[icon] = CTkImage(
            dark_image=self.get_light_icon(icon_image_raw),
            light_image=icon_image_raw,
        )

        return self.cache[icon]
