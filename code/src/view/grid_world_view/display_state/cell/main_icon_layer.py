from typing import Optional

from PIL.Image import Image

from src.model.dynamics.actions import Action
from src.model.learning_system.cell_configuration import DisplayMode
from src.model.state.cell_entities import CellEntity
from src.view.grid_world_view.display_state.cell.base_layer import BaseLayer


class MainIconLayer(BaseLayer):
    """The layer responsible for drawing the background of the cell."""

    def draw(self):
        """Draw the main icon."""
        size = self.cell_layout.get_bounding_box_size(self.bounding_box)
        icon = self.__get_main_icon(size)
        if icon is None:
            return
        self.draw_icon(icon, size)

    def __get_main_icon(self, size: int) -> Optional[Image]:
        """Get what the main icon should be based upon the cell config.

        Args:
            size (int): the size the icon should be.

        Returns:
            Image: the image that corresponds to what the main icon should be
        """
        config = self.config
        loader = self.icon_loader
        match config.display_mode:
            case DisplayMode.default | DisplayMode.state_value:
                return loader.get_cell_entity_icon(config.cell_entity, size)
            case (
                DisplayMode.action_value_global | DisplayMode.action_value_local
            ):
                if config.cell_entity is CellEntity.goal:
                    return loader.get_cell_entity_icon(config.cell_entity, size)
                return None
            case DisplayMode.best_action:
                best_action = self.__get_best_action()
                if best_action is None:
                    return loader.get_cell_entity_icon(config.cell_entity, size)

                return loader.get_action_icon(best_action, size)

    def __get_best_action(self) -> Optional[Action]:
        """Get the action that has the best value.

        Returns:
            Optional[Action]: the best action if there is one.
        """
        action_values = self.config.action_values_raw
        best_action_value = float("-inf")
        best_action = None
        for action in Action:
            action_value = action_values[action]
            if action_value is None:
                continue
            if best_action_value is None:
                best_action_value = action_value
                best_action = action
            elif action_value > best_action_value:
                best_action_value = action_value
                best_action = action
        return best_action
