from typing import Dict, Optional

from src.model.dynamics.actions import Action
from src.model.state.cell_entities import CellEntity


class CellConfiguration(object):
    """Class to represent the configuration of a cell in a given state."""

    def __init__(
        self,
        cell_value: Optional[float],
        action_values: Dict[Action, Optional[float]],
        cell_entity: CellEntity,
    ) -> None:
        """Create cell configuration.

        Args:
            cell_value (float): the value the cell should represent in its
            background.
            action_values (Dict[Action, float]): the value of different actions
            in this cell.
            cell_entity (CellEntity): the entity to display in this cell
        """
        self.cell_value = cell_value
        self.action_values = action_values
        self.cell_entity = cell_entity
