from src.model.dynamics.actions import Action
from src.model.dynamics.grid_world import GridWorld
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
    action_value_description,
)
from src.view.display_state_v2.cell.base_layer import BaseLayer


class ArrowLayer(BaseLayer):
    """The layer responsible for drawing the background of the cell."""

    def draw(self):
        """Draw the arrow layer."""
        match self.options.display_mode:
            case DisplayMode.action_value_global:
                self.__draw_specific_arrows(
                    self.config.action_values_normalised
                )
            case DisplayMode.action_value_local:
                self.__draw_specific_arrows(
                    self.__rescale_values_locally(
                        self.config.action_values_raw
                    ),
                )
            case _:
                return

    def __draw_specific_arrows(self, action_values: action_value_description):
        for action, action_value in action_values.items():
            if action_value is not None:
                self.__draw_arrow(action, action_value)

    def __draw_arrow(self, action: Action, action_value: float):
        size = self.cell_layout.get_bounding_box_size(self.bounding_box) // 3
        color = self.value_to_color(action_value)
        icon = self.icon_loader.get_action_icon(action, size, color)

        dir_x, dir_y = GridWorld.action_direction[action]

        relative_position = ((dir_x + 1) / 2, (dir_y + 1) / 2)
        self.draw_icon(icon, size, relative_position)

    def __rescale_values_locally(
        self, action_values: action_value_description
    ) -> action_value_description:
        """Rescale the action values in this cell 0-1.

        this should only be based on the values in this cell rather than the
        global range of values.

        Args:
            action_values (action_value_description): the action values of this
                cell.

        Returns:
            action_value_description: the scaled action values in the range 0-1
        """
        min_value = float("inf")
        max_value = float("-inf")

        for action_value in action_values.values():
            if action_value is None:
                continue
            min_value = min(action_value, min_value)
            max_value = max(action_value, max_value)

        rescaled_values: action_value_description = {}
        value_range = max_value - min_value
        for action, action_value in action_values.items():
            if action_value is None:
                rescaled_values[action] = None
                continue
            rescaled_values[action] = (action_value - min_value) / value_range
        return rescaled_values
