from typing import Tuple

from src.model.dynamics.actions import Action

from ..dynamics.base_dynamics import BaseDynamics
from ..state.cell_entities import CellEntity
from .cell_configuration import (
    CellConfiguration,
    DisplayMode,
    action_value_description,
)
from .value_range_normaliser.normaliser import StateValueNormaliser


class StateDescription(object):
    """Compile together the dynamic static state information."""

    def __init__(
        self,
        dynamics: BaseDynamics,
        state: int,
        normaliser: StateValueNormaliser,
        display_mode: DisplayMode,
    ) -> None:
        """Initiate this state description.

        Args:
            dynamics (BaseDynamics): the dynamics this state is a part of
            state (int): the state to describe
            normaliser (StateValueNormaliser): the state value normaliser
            allowing for visualisations of the current state value table.
            display_mode (DisplayMode): how to display this state.
        """
        self.grid_world = dynamics.grid_world
        self.state = dynamics.state_pool.get_state_from_id(state)
        self.normaliser = normaliser
        self.display_mode = display_mode

    def cell_configuration(self, cell: tuple[int, int]) -> CellConfiguration:
        """Get the configuration of a cell in a given state.

        Args:
            cell (tuple[int, int]): the cell to check.

        Returns:
            CellConfiguration: the cell's configuration
        """
        normalised_action_values, raw_action_values = self.cell_action_values(
            cell
        )

        return CellConfiguration(
            self.normaliser.get_state_value_normalised(cell),
            normalised_action_values,
            self.normaliser.get_state_value_raw(cell),
            raw_action_values,
            cell,
            self.cell_entity(cell),
            self.display_mode,
        )

    def cell_action_values(
        self, cell: tuple[int, int]
    ) -> Tuple[action_value_description, action_value_description]:
        """Get the value of actions in this given cell.

        Args:
            cell (tuple[int, int]): the location of the cell to check.

        Returns:
            Dict[Action, float]: mapping from the action to its value
        """
        action_values_normalised: action_value_description = {}
        action_values_raw: action_value_description = {}
        for action in Action:
            action_values_normalised[
                action
            ] = self.normaliser.get_state_action_value_normalised(cell, action)
            action_values_raw[
                action
            ] = self.normaliser.get_state_action_value_raw(cell, action)

        return action_values_normalised, action_values_raw

    def cell_entity(self, cell: tuple[int, int]) -> CellEntity:
        """Get the cell entity at a given location.

        Args:
            cell (tuple[int, int]): the location of the cell to check.

        Raises:
            ValueError: if the cell is not a valid location

        Returns:
            CellEntity: the cell entity at this location
        """
        if not self.grid_world.is_in_bounds(cell):
            raise ValueError(f"location {cell} is not in bounds")

        if cell == self.state.agent_location:
            return CellEntity.agent

        return self.state.entities.get(cell, CellEntity.empty)
