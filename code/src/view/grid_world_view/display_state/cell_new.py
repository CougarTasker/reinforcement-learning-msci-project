from typing import Tuple

from colour import Color
from PIL.ImageDraw import ImageDraw

from src.model.learning_system.cell_configuration import (
    CellConfiguration,
    DisplayMode,
)
from src.model.state.cell_entities import CellEntity


class Cell(object):
    """Widget to display an individual cell."""

    padding = 8
    default_background_color = "#515151"

    def __init__(
        self,
        config: CellConfiguration,
        bounding_box: Tuple[int, int, int, int],
    ) -> None:
        """Initialise the cell.

        displays the cell as a rounded rectangle with icons.

        Args:
            config (CellConfiguration): the configuration of how this cell
            should present.
            bounding_box (Tuple[int, int, int, int]): the position and size of
            this cell on the canvas.
        """
        self.config = config
        self.bounding_box = bounding_box

    def draw(self, image_draw: ImageDraw):
        """Draw the cell to the canvas.

        Args:
            image_draw (ImageDraw): the drawing context
        """
        self.__draw_background(image_draw)

    def __draw_background(self, image_draw: ImageDraw):
        fill, outline = self.__cell_mode_color()

        image_draw.rounded_rectangle(
            self.bounding_box,
            self.padding,
            fill=fill,
            outline=outline,
            width=self.padding,
        )

    def __cell_mode_color(self) -> Tuple[str, str]:
        """Get the color for the inner and outer background based on the mode.

        Returns:
            Tuple[str, str]: inner and outer color
        """
        default_color = self.default_background_color
        if self.config.display_mode is not DisplayMode.state_value:
            return default_color, default_color
        cell_value_color = self.__cell_color()

        if self.config.cell_entity is CellEntity.empty:
            return cell_value_color, cell_value_color

        return default_color, cell_value_color

    def __cell_color(self) -> str:
        """Get the color the cell should be based upon the value.

        red represents a low value and green represents a good value

        Returns:
            str: the hex color of the cell based on this value.
        """
        cell_value = self.config.cell_value_normalised
        if cell_value is None:
            return self.default_background_color

        # I know red is zero but this allows for more configuration
        start = Color("red").get_hue()
        end = Color("green").get_hue()

        hue = cell_value * (end - start) + start

        return Color(hsl=(hue, 1, 0.5)).hex_l
