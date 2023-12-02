from typing import Tuple

from colour import Color
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from src.model.learning_system.cell_configuration import CellConfiguration
from src.view.grid_world_view.display_state.cell.cell_layout import CellLayout
from src.view.icons.load_icon import IconLoader


class BaseLayer(object):
    """Represents one layer of the cell's drawing."""

    def __init__(  # Noqa : WPS211
        self,
        config: CellConfiguration,
        canvas: Image,
        drawing_context: ImageDraw,
        bounding_box: Tuple[int, int, int, int],
        cell_layout: CellLayout,
    ) -> None:
        """Initialise the layer.

        Args:
            config (CellConfiguration): the configuration to represent
            canvas (Image): the canvas to draw on
            drawing_context (ImageDraw): the drawing context of this canvas
            bounding_box (Tuple[int, int, int, int]): the area of the canvas
            this layer should be drawn in.
            cell_layout (CellLayout): the layout of the entire cell.
        """
        self.config = config
        self.canvas = canvas
        self.drawing_context = drawing_context
        self.bounding_box = bounding_box
        self.cell_layout = cell_layout
        self.icon_loader = IconLoader()

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

        icon_alpha = icon.split()[3]
        self.canvas.paste(icon, location, icon_alpha)

    def value_to_color(self, worth: float) -> str:
        """Convert a floating point value to a color.

        Args:
            worth (float): the value to represent in the range 0 to 1.

        Returns:
            str: the color in a hexadecimal string representation
        """
        # I know red is zero but this allows for more configuration
        start = Color("red").get_hue()
        end = Color("green").get_hue()

        hue = worth * (end - start) + start

        return Color(hsl=(hue, 1, 0.5)).hex_l
