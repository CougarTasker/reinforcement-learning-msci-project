from enum import Enum
from typing import Dict, Optional, Tuple

from src.model.dynamics.actions import Action
from src.model.state.cell_entities import CellEntity


class DisplayMode(Enum):
    """Enumerates the different possible display styles."""

    default = 0
    state_value = 1
    action_value_global = 2
    action_value_local = 3
    best_action = 4


action_value_description = Dict[Action, Optional[float]]


class CellConfiguration(object):  # noqa: WPS230 TODO refactor this
    """Class to represent the configuration of a cell in a given state."""

    def __init__(  # noqa: WPS211 TODO refactor this
        self,
        cell_value_normalised: Optional[float],
        action_values_normalised: action_value_description,
        cell_value_raw: Optional[float],
        action_values_raw: action_value_description,
        location: Tuple[int, int],
        cell_entity: CellEntity,
        display_mode: DisplayMode,
    ) -> None:
        """Create cell configuration.

        Args:
            cell_value_normalised (float): the value the cell should represent
            in its background.
            action_values_normalised (action_value_description): the value of
            different actions in this cell. normalised globally 0-1
            cell_value_raw (Optional[float]): the value the cell should report
            in the tooltip.
            action_values_raw (action_value_description): the value of
            different actions in this cell. un-normalised for use in the tooltip
            location (Tuple[int, int]): where the cell is in the grid.
            cell_entity (CellEntity): the entity to display in this cell
            display_mode (DisplayMode): how the cell should display its
            information.
        """
        self.cell_value_normalised = cell_value_normalised
        self.action_values_normalised = action_values_normalised
        self.cell_value_raw = cell_value_raw
        self.action_values_raw = action_values_raw
        self.location = location
        self.cell_entity = cell_entity
        self.display_mode = display_mode
