from enum import Enum
from os import path
from typing import Dict, Tuple

import numpy as np
from customtkinter import CTkImage
from PIL import Image as Pillow
from PIL.Image import Image

from src.model.dynamics.actions import Action
from src.model.state.cell_entities import CellEntity


class Icon(Enum):
    """Enumerates all possible icons available."""

    robot = "robot"
    flag = "flag"
    no_entry = "do-not-enter"
    up_arrow = "up-arrow"
    down_arrow = "down-arrow"
    right_arrow = "right-arrow"
    left_arrow = "left-arrow"
    empty = "empty"


class IconLoader(object):
    """Load Icon images into the application."""

    _instance = None

    # icon -> normal icon, light icon
    # avoid loading the same icon file multiple times
    bitmap_cache: Dict[Icon, Tuple[Image, Image]] = {}

    # each different size of an icon requires its own image object this helps
    # avoid duplicates
    tkinter_size_cache: Dict[Tuple[Icon, int], CTkImage] = {}

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
        img_array = np.array(image.convert("RGBA"))

        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        non_transparent_pixels = alpha != 0
        # set icon color to wight
        rgb[non_transparent_pixels] = [255, 255, 255]

        return Pillow.fromarray(img_array)

    action_mapping: Dict[Action, Icon] = {
        Action.up: Icon.up_arrow,
        Action.down: Icon.down_arrow,
        Action.left: Icon.left_arrow,
        Action.right: Icon.right_arrow,
    }

    def get_action_icon(self, action: Action, size: int) -> CTkImage:
        """Get the appropriate arrow icon for a given action.

        Args:
            action (Action): the action to represent
            size (int): the size the icon should be displayed by tkinter

        Returns:
            CTkImage: the image pointing in that actions direction.
        """
        return self.get_icon(self.action_mapping[action], size)

    cell_entity_mapping = {
        CellEntity.agent: Icon.robot,
        CellEntity.goal: Icon.flag,
        CellEntity.blocked: Icon.no_entry,
        CellEntity.empty: Icon.empty,
    }

    def get_cell_entity_icon(self, entity: CellEntity, size: int) -> CTkImage:
        """Get the appropriate icon for a given cell entity.

        Args:
            entity (CellEntity): the entity to represent
            size (int): the size the icon should be displayed by tkinter

        Returns:
            CTkImage: the image of this cell entity
        """
        return self.get_icon(self.cell_entity_mapping[entity], size)

    def get_icon(self, icon: Icon, size: int) -> CTkImage:
        """Get the custom tkinter image object for a given icon.

        Args:
            icon (Icon): the icon to display
            size (int): the size the icon should be displayed by tkinter

        Returns:
            CTkImage: the image representing this icon in light and dark themes
        """
        cache_key = (icon, size)
        existing_image = self.tkinter_size_cache.get(cache_key, None)
        if existing_image is not None:
            return existing_image

        dark_image_raw, light_image_raw = self.__get_icon_raw_files(icon)

        # swapping icon styles for contrast
        tkinter_image = CTkImage(
            dark_image=light_image_raw,
            light_image=dark_image_raw,
            size=(size, size),
        )
        self.tkinter_size_cache[cache_key] = tkinter_image

        return tkinter_image

    def __get_icon_raw_files(self, icon: Icon) -> Tuple[Image, Image]:
        cached_file = self.bitmap_cache.get(icon, None)
        if cached_file is not None:
            return cached_file

        dark_image_raw = Pillow.open(self.get_path(icon))
        light_image_raw = self.get_light_icon(dark_image_raw)

        icon_raw = (dark_image_raw, light_image_raw)
        self.bitmap_cache[icon] = icon_raw
        return icon_raw
