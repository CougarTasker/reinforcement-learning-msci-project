from typing import Tuple

from src.model.agents.base_agent import BaseAgent
from src.model.agents.value_iteration.agent import ValueIterationAgent
from src.model.dynamics.actions import Action
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.learning_system.cell_configuration import (
    CellConfiguration,
    DisplayMode,
    action_value_description,
)
from src.model.learning_system.state_description.cell_state_lookup import (
    CellStateLookup,
)
from src.model.state.cell_entities import CellEntity
from src.model.state.state_instance import StateInstance

from .state_description import StateDescription
from .value_range_normaliser.normaliser import StateValueNormaliser
from .value_range_normaliser.normaliser_factory import NormaliserFactory


class StateDescriptionFactory(object):
    """Factory for creating state descriptions."""

    def __init__(
        self,
        agent: BaseAgent,
        dynamics: BaseDynamics,
        display_mode: DisplayMode,
    ) -> None:
        """Initialise the state Description factory.

        Args:
            agent (BaseAgent): the agent, used to get get the cell values.
            dynamics (BaseDynamics): the dynamics the state is in.
            display_mode (DisplayMode): the display_mode of the cell.
        """
        self.agent = agent
        self.dynamics = dynamics
        self.grid_world = dynamics.grid_world
        self.cell_state_lookup = CellStateLookup(dynamics)
        self.value_normalisation_factory = NormaliserFactory(
            self.agent,
            self.dynamics,
            isinstance(self.agent, ValueIterationAgent),
        )
        self.display_mode = display_mode

    def create_state_description(self, state_id: int) -> StateDescription:
        """Get a state description for this state ID.

        Args:
            state_id (int): the state to represent in the view

        Returns:
            StateDescription: the state description
        """
        normaliser = self.value_normalisation_factory.create_normaliser(
            state_id
        )
        state = self.dynamics.state_pool.get_state_from_id(state_id)
        config = {
            cell: self.__cell_configuration(state, normaliser, cell)
            for cell in self.grid_world.list_cells()
        }

        return StateDescription(
            self.grid_world, state, config, self.display_mode
        )

    def __cell_configuration(
        self,
        reference_state: StateInstance,
        normaliser: StateValueNormaliser,
        cell: Tuple[int, int],
    ) -> CellConfiguration:
        """Get the configuration of a cell in a given state.

        Args:
            state (StateInstance): the state that this cell is in.
            normaliser (StateValueNormaliser): normaliser to get value
            cell (tuple[int, int]): the cell to check.

        Returns:
            CellConfiguration: the cell's configuration
        """
        action_values_normalised: action_value_description = {}
        action_values_raw: action_value_description = {}

        cell_state = self.cell_state_lookup.get_state(reference_state, cell)

        if cell_state is None:
            for action in Action:
                action_values_normalised[action] = None
                action_values_raw[action] = None

            return CellConfiguration(
                None,
                action_values_normalised,
                None,
                action_values_raw,
                cell,
                self.__cell_entity(reference_state, cell),
                self.display_mode,
            )

        cell_state_id = self.dynamics.state_pool.get_state_id(cell_state)
        for action in Action:
            action_values_normalised[
                action
            ] = normaliser.get_state_action_value_normalised(cell_state, action)
            action_values_raw[action] = self.agent.get_state_action_value(
                cell_state_id, action
            )

        return CellConfiguration(
            normaliser.get_state_value_normalised(cell_state),
            action_values_normalised,
            self.agent.get_state_value(cell_state_id),
            action_values_raw,
            cell,
            self.__cell_entity(reference_state, cell),
            self.display_mode,
        )

    def __cell_entity(
        self, state: StateInstance, cell: tuple[int, int]
    ) -> CellEntity:
        """Get the cell entity at a given location.

        Args:
            state (StateInstance): the state the cell is in.
            cell (tuple[int, int]): the location of the cell to check.

        Raises:
            ValueError: if the cell is not a valid location

        Returns:
            CellEntity: the cell entity at this location
        """
        if not self.grid_world.is_in_bounds(cell):
            raise ValueError(f"location {cell} is not in bounds")

        if cell == state.agent_location:
            return CellEntity.agent

        return state.entities.get(cell, CellEntity.empty)
