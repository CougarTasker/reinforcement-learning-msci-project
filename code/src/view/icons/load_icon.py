from dataclasses import dataclass
from enum import Enum
from os import path
from typing import Dict, Tuple

import numpy as np
from PIL import Image as Pillow
from PIL.Image import Image
from typing_extensions import Self

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


rgb_type = Tuple[int, int, int]


@dataclass(frozen=True)
class IconVariantSpecification(object):
    """Specifies a particular variant of an icon for cacheing purposes."""

    icon_type: Icon
    size: int
    color: rgb_type


class IconLoader(object):
    """Load Icon images into the application."""

    _instance = None

    # icon -> normal icon, light icon
    # avoid loading the same icon file multiple times
    bitmap_cache: Dict[Icon, Image] = {}

    # cache icon size and color because they will likely be used a lot
    variant_cache: Dict[IconVariantSpecification, Image] = {}

    default_color = (255, 255, 255)

    def __new__(cls) -> Self:
        """Create a config object.

        Overridden to provide the singleton patten, there must only be one
        IconLoader object. there should only be one cache so there is not need
        for more than one loader

        Returns:
            Self: The config object with the loaded data
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

    rgb_component_max = 255

    def get_coloured_icon(
        self, image: Image, color: Tuple[int, int, int]
    ) -> Image:
        """Convert a black icon to a specific color.

        sets all non-transparent pixels to the color.

        Args:
            image (Image): the image to convert,
            color (str): must represent a valid color

        Returns:
            Image: the image with a white foreground
        """
        np_color = np.array(color, dtype=int)

        img_array = np.array(image.convert("RGBA"))

        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        non_transparent_pixels = alpha != 0
        # set icon color to wight
        rgb[non_transparent_pixels] = np_color

        return Pillow.fromarray(img_array)

    action_mapping: Dict[Action, Icon] = {
        Action.up: Icon.up_arrow,
        Action.down: Icon.down_arrow,
        Action.left: Icon.left_arrow,
        Action.right: Icon.right_arrow,
    }

    def get_action_icon(
        self,
        action: Action,
        size: int,
        color: Tuple[int, int, int] = default_color,
    ) -> Image:
        """Get the appropriate arrow icon for a given action.

        Args:
            action (Action): the action to represent
            size (int): the size the icon should be displayed by tkinter
            color (str): the color of the icon

        Returns:
            Image: the image pointing in that actions direction.
        """
        return self.get_icon(self.action_mapping[action], size, color)

    cell_entity_mapping = {
        CellEntity.agent: Icon.robot,
        CellEntity.goal: Icon.flag,
        CellEntity.warning: Icon.no_entry,
        CellEntity.empty: Icon.empty,
    }

    def get_cell_entity_icon(
        self,
        entity: CellEntity,
        size: int,
        color: Tuple[int, int, int] = default_color,
    ) -> Image:
        """Get the appropriate icon for a given cell entity.

        Args:
            entity (CellEntity): the entity to represent
            size (int): the size the icon should be displayed by tkinter
            color (str): the color of the icon

        Returns:
            Image: the image of this cell entity
        """
        return self.get_icon(self.cell_entity_mapping[entity], size, color)

    def get_icon(
        self,
        icon: Icon,
        size: int,
        color: Tuple[int, int, int] = default_color,
    ) -> Image:
        """Get the custom tkinter image object for a given icon.

        Args:
            icon (Icon): the icon to display
            size (int): the size the icon should be displayed by tkinter
            color (str): the color of the icon

        Returns:
            Image: the image representing this icon
        """
        size = max(size, 1)
        cache_key = IconVariantSpecification(icon, size, color)
        existing_image = self.variant_cache.get(cache_key, None)
        if existing_image is not None:
            return existing_image

        image_raw = self.__get_icon_raw_files(icon)

        coloured_icon = self.get_coloured_icon(image_raw, color)
        # resize image
        coloured_icon.thumbnail((size, size))

        self.variant_cache[cache_key] = coloured_icon

        return coloured_icon

    def __get_icon_raw_files(self, icon: Icon) -> Image:
        cached_file = self.bitmap_cache.get(icon, None)
        if cached_file is not None:
            return cached_file

        icon_raw = Pillow.open(self.get_path(icon))

        self.bitmap_cache[icon] = icon_raw
        return icon_raw
