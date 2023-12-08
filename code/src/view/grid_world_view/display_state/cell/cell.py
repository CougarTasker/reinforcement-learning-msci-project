from typing import Tuple

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from src.model.learning_system.cell_configuration import CellConfiguration
from src.view.grid_world_view.display_state.cell.arrow_layer import ArrowLayer
from src.view.grid_world_view.display_state.cell.background_layer import (
    BackgroundLayer,
)
from src.view.grid_world_view.display_state.cell.cell_layout import CellLayout
from src.view.grid_world_view.display_state.cell.main_icon_layer import (
    MainIconLayer,
)


class Cell(object):
    """Widget to display an individual cell."""

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
        self.cell_layout = CellLayout(bounding_box)

    def draw(
        self,
        canvas: Image,
        drawing_context: ImageDraw,
    ):
        """Draw the cell to the canvas.

        Args:
            canvas (Image): the image to draw to
            drawing_context (ImageDraw): the drawing context
        """
        BackgroundLayer(
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.bounding_box,
            self.cell_layout,
        ).draw()
        MainIconLayer(
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.inset_bounding_box(
                self.cell_layout.padding + self.cell_layout.border_width
            ),
            self.cell_layout,
        ).draw()
        ArrowLayer(
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.inset_bounding_box(self.cell_layout.padding),
            self.cell_layout,
        ).draw()
