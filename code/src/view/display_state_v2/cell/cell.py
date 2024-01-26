from typing import Tuple

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from src.model.learning_system.cell_configuration.cell_configuration import (
    CellConfiguration,
)
from src.model.learning_system.global_options import GlobalOptions

from .arrow_layer import ArrowLayer
from .background_layer import BackgroundLayer
from .cell_layout import CellLayout
from .main_icon_layer import MainIconLayer


class Cell(object):
    """Widget to display an individual cell."""

    def __init__(
        self,
        options: GlobalOptions,
        config: CellConfiguration,
        bounding_box: Tuple[int, int, int, int],
    ) -> None:
        """Initialise the cell.

        displays the cell as a rounded rectangle with icons.

        Args:
            options (GlobalOptions): the global configuration used in rendering
                each cell.
            config (CellConfiguration): the configuration of how this cell
                should present.
            bounding_box (Tuple[int, int, int, int]): the position and size of
                this cell on the canvas.
        """
        self.config = config
        self.options = options
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
            self.options,
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.bounding_box,
            self.cell_layout,
        ).draw()
        MainIconLayer(
            self.options,
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.inset_bounding_box(
                self.cell_layout.padding + self.cell_layout.border_width
            ),
            self.cell_layout,
        ).draw()
        ArrowLayer(
            self.options,
            self.config,
            canvas,
            drawing_context,
            self.cell_layout.inset_bounding_box(self.cell_layout.padding),
            self.cell_layout,
        ).draw()
