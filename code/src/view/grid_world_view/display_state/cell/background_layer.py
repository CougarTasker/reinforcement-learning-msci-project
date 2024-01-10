from typing import Tuple

from src.model.learning_system.cell_configuration import DisplayMode
from src.model.state.cell_entities import CellEntity
from src.view.grid_world_view.display_state.cell.base_layer import (
    BaseLayer,
    rgb_type,
)


class BackgroundLayer(BaseLayer):
    """The layer responsible for drawing the background of the cell."""

    default_background_color: rgb_type = (80, 80, 80)

    def draw(self):
        """Draw the background layer."""
        fill, outline = self.__cell_mode_color()

        self.drawing_context.rounded_rectangle(
            self.bounding_box,
            self.cell_layout.border_width,
            fill=fill,
            outline=outline,
            width=self.cell_layout.border_width,
        )

    def __cell_mode_color(
        self,
    ) -> Tuple[rgb_type, rgb_type]:
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

    def __cell_color(self) -> rgb_type:
        """Get the color the cell should be based upon the value.

        red represents a low value and green represents a good value

        Returns:
            rgb_type: the hex color of the cell based on this value.
        """
        cell_value = self.config.cell_value_normalised
        if cell_value is None:
            return self.default_background_color
        return self.value_to_color(cell_value)
