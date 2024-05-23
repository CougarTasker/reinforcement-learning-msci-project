from typing import Dict, Optional

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QStackedLayout,
    QWidget,
)
from typing_extensions import override

from src.model.dynamics.grid_world import integer_position
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.display_state_v2.cell.cell import Cell
from src.view.visibility_observer import BaseVisibilityObserver


class DisplayState(BaseVisibilityObserver):
    """Widget for displaying a given grid world state."""

    padding = 10

    cell_margins = 0.1
    background_color = (200, 200, 200, 0)

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Initialise the state display.

        this widget will display a given state and update it on request.

        Args:
            parent (QWidget): the parent of this widget.
        """
        super().__init__(parent)

        outer_layout, overlay_layout = self.__setup_layouts()
        self.overlay_layout = overlay_layout

        self.overlay_widgets: Dict[integer_position, QWidget] = {}
        self.overlay_layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
            ),
            0,
            0,
        )
        self.spacer_widget = QSpacerItem(
            0, 0, QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )
        self.overlay_layout.addItem(self.spacer_widget, 1, 1)

        self.image_label = QLabel(self)
        self.image_label.setContentsMargins(0, 0, 0, 0)
        self.image_label.setStyleSheet("border: 0;")
        outer_layout.addWidget(self.image_label)

        self.state: Optional[StateDescription] = None

    @override
    def visible_state_updated(self, state: StateDescription):
        """Handle state update events.

        Args:
            state (StateDescription): the new state

        """
        self.state = state
        self.__configure_grid()
        self.__populate_overlay()

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
        self.__populate_overlay()

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
        width = self.image_label.contentsRect().width() - self.padding
        height = self.image_label.contentsRect().height() - self.padding
        return width, height

    def __populate_overlay(self):
        state = self.state
        if state is None:
            return

        width, height = self.__get_current_size()
        (
            offset_min_x,
            offset_min_y,
            offset_max_x,
            offset_max_y,
        ) = state.grid_world.get_grid_bounds(width, height, self.cell_margins)
        self.overlay_layout.removeItem(self.spacer_widget)
        self.overlay_layout.addItem(
            self.spacer_widget,
            state.grid_world.height + 1,
            state.grid_world.width + 1,
        )

        self.overlay_layout.setColumnMinimumWidth(0, offset_min_x)
        self.overlay_layout.setRowMinimumHeight(0, offset_min_y)
        self.overlay_layout.setColumnMinimumWidth(
            state.grid_world.width + 1, offset_min_x
        )
        self.overlay_layout.setRowMinimumHeight(
            state.grid_world.height + 1, offset_min_y
        )

        for position in state.grid_world.list_cells():
            widget = self.overlay_widgets.get(position, None)
            if widget is None:
                widget = QWidget()
                self.overlay_layout.addWidget(
                    widget, position[1] + 1, position[0] + 1
                )
                self.overlay_widgets[position] = widget

            widget.setToolTip(state.cell_config[position].tooltip_text)

    def __setup_layouts(self):
        outer_layout = QStackedLayout(self)
        outer_layout.setSpacing(0)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.setContentsMargins(0, 0, 0, 0)

        overlay_widget = QWidget(self)
        outer_layout.addWidget(overlay_widget)
        overlay_layout = QGridLayout(overlay_widget)
        overlay_widget.setStyleSheet("background-color:rgba(0, 0, 0, 0);")
        overlay_layout.setVerticalSpacing(1)
        overlay_layout.setHorizontalSpacing(1)

        return outer_layout, overlay_layout
