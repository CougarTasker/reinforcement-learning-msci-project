from typing import Optional

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from typing_extensions import override

from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.display_state_v2.cell.cell import Cell
from src.view.visibility_observer import BaseVisibilityObserver


class DisplayState(BaseVisibilityObserver):
    """Widget for displaying a given grid world state."""

    cell_margins = 0.1
    background_color = (200, 200, 200, 0)

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Initialise the state display.

        this widget will display a given state and update it on request.

        Args:
            parent (QWidget): the parent of this widget.
        """
        super().__init__(parent)

        self.image_label = QLabel(self)
        self.image_label.setContentsMargins(0, 0, 0, 0)
        self.image_label.setStyleSheet("border: 0;")
        self.setContentsMargins(0, 0, 0, 0)

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label, 0, 0)

        self.state: Optional[StateDescription] = None

    @override
    def visible_state_updated(self, state: StateDescription):
        """Handle state update events.

        Args:
            state (StateDescription): the new state

        """
        self.state = state
        self.__configure_grid()

    @override
    def resizeEvent(  # noqa: N802 built in method to base class
        self, event: QResizeEvent
    ):
        """Handle resize event.

        resize the inner grid based upon the updated dimensions.

        Args:
            event (QResizeEvent): the resize event
        """
        self.__configure_grid()

    def __make_blank_image(self):
        size = self.__get_current_size()
        image_mode = "RGBA"
        image = Image.new(image_mode, size, self.background_color)
        image_draw = ImageDraw.Draw(image, image_mode)
        return image, image_draw

    def __configure_grid(self):
        if self.state is None:
            return
        width, height = self.__get_current_size()
        expected_cell_size = self.state.grid_world.get_cell_sizing(
            width, height, self.cell_margins
        )[0]
        if expected_cell_size < 10:
            # cells are too small
            return
        self.__populate_cells(self.state)
        image, image_draw = self.__make_blank_image()

        for cell in self.cells.values():
            cell.draw(image, image_draw)

        self.image_label.setPixmap(QPixmap.fromImage(ImageQt(image)))

    def __populate_cells(
        self,
        state: StateDescription,
    ):
        self.cells = {}
        width, height = self.__get_current_size()
        cell_positions = state.grid_world.list_cell_positions(
            width, height, self.cell_margins
        )

        for cell_position in cell_positions:
            (
                cell_coordinate,
                bounding_box,
            ) = cell_position
            self.cells[cell_coordinate] = Cell(
                state.global_options,
                state.cell_config[cell_coordinate],
                bounding_box,
            )

    def __get_current_size(self):
        width = self.image_label.contentsRect().width() - 2
        height = self.image_label.contentsRect().height() - 2
        return width, height
