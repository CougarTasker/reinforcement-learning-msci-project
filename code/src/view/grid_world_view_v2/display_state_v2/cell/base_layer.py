from colorsys import hls_to_rgb
from dataclasses import dataclass
from typing import Tuple

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from src.model.learning_system.cell_configuration.cell_configuration import (
    CellConfiguration,
)
from src.model.learning_system.global_options import GlobalOptions
from src.view.grid_world_view_v2.display_state_v2.cell.cell_layout import (
    CellLayout,
)
from src.view.icons.load_icon import IconLoader, rgb_type


@dataclass(slots=True, frozen=True)
class BaseLayer(object):
    """Represents one layer of the cell's drawing."""

    options: GlobalOptions
    config: CellConfiguration
    canvas: Image
    drawing_context: ImageDraw
    bounding_box: Tuple[int, int, int, int]
    cell_layout: CellLayout
    icon_loader = IconLoader()

    def draw(self):
        """Draw this layer to the canvas.

        Raises:
            RuntimeError: if this method is not overridden.
        """
        raise RuntimeError("Draw should be overridden by concrete class")

    def draw_icon(
        self,
        icon: Image,
        size: int,
        rel_pos: Tuple[float, float] = (0.5, 0.5),
    ):
        """Draw an icon in the cell.

        rel_pos is relative to the bounding box of this layer.

        Args:
            icon (Image): the icon to display
            size (int): the size of the icon to display
            rel_pos (Tuple[float, float], optional): the position in the cell.
                Defaults to the centre.
        """
        min_x, min_y, max_x, _max_y = self.bounding_box
        rel_x, rel_y = rel_pos

        space = max_x - min_x - size
        location = (
            min_x + int(rel_x * space),
            min_y + int(rel_y * space),
        )

        icon_alpha = icon.getchannel("A")
        self.canvas.paste(icon, location, icon_alpha)

    def value_to_color(self, worth: float) -> rgb_type:
        """Convert a floating point value to a color.

        Args:
            worth (float): the value to represent in the range 0 to 1.

        Returns:
            rgb_type: the color as rgb values in the range 0-255
        """
        hue = worth / 3  # Range from red to green
        saturation = 1.0
        lightness = 0.5
        color_range = 255

        red, green, blue = hls_to_rgb(hue, lightness, saturation)
        return (
            int(color_range * red),
            int(color_range * green),
            int(color_range * blue),
        )
