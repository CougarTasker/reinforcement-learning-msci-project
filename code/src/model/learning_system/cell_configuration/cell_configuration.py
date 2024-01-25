from dataclasses import dataclass
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


@dataclass(frozen=True)
class CellConfiguration(object):
    """Class to represent the configuration of a cell in a given state."""

    action_values_normalised: action_value_description
    action_values_raw: action_value_description
    location: Tuple[int, int]
    cell_entity: CellEntity
    cell_value_normalised: Optional[float] = None
    cell_value_raw: Optional[float] = None

    @property
    def tooltip_text(self) -> str:
        """Gets the text for a tooltip on hovering over the cell.

        Returns:
            str: the text to display to the user for extra information
        """
        text = f"cell={self.location}"
        if self.cell_value_raw is not None:
            text += f"\ncell value={self.cell_value_raw:.4f}"

        for action in Action:
            action_value = self.action_values_raw[action]
            if action_value is not None:
                text += f"\n{action.name} value = {action_value:.4f}"
        return text
