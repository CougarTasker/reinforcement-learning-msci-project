from typing import Dict, Tuple

from typing_extensions import override

from src.model.dynamics.actions import Action
from src.model.dynamics.grid_world import integer_position
from src.model.learning_system.base_entity_decorator import BaseEntityDecorator
from src.model.learning_system.top_level_entities.container import (
    EntityContainer,
)
from src.model.learning_system.value_standardisation.normaliser import (
    StateValueNormaliser,
)
from src.model.learning_system.value_standardisation.normaliser_factory import (
    NormaliserFactory,
)
from src.model.state.cell_entities import CellEntity
from src.model.state.state_instance import StateInstance

from .cell_configuration import CellConfiguration, action_value_description
from .cell_state_lookup import CellStateLookup


class CellConfigurationFactory(BaseEntityDecorator):
    """Factory for creating cell configurations."""

    def __init__(self, entities: EntityContainer) -> None:
        """Initialise the state Description factory.

        Args:
            entities (EntityContainer): The entities the cell configuration is
                based upon.
        """
        super().__init__(entities)
        self.update_entities(entities)

    @override
    def update_entities(self, entities: EntityContainer) -> None:
        """Update the entities used by this decorator.

        Args:
            entities (EntityContainer): the new entities to use.
        """
        super().update_entities(entities)
        self.cell_state_lookup = CellStateLookup(entities.dynamics)
        self.value_normalisation_factory = NormaliserFactory(
            entities.agent,
            entities.dynamics,
            enable_cache=False,
        )

    def get_cell_configuration(
        self, state_id: int
    ) -> Dict[integer_position, CellConfiguration]:
        """Get a state description for this state ID.

        Args:
            state_id (int): the state to represent in the view

        Returns:
            StateDescription: the state description
        """
        normaliser = self.value_normalisation_factory.create_normaliser(
            state_id
        )
        state = self.state_pool.get_state_from_id(state_id)
        return {
            cell: self.__cell_configuration(state, normaliser, cell)
            for cell in self.entities.dynamics.grid_world.list_cells()
        }

    def __cell_configuration(
        self,
        reference_state: StateInstance,
        normaliser: StateValueNormaliser,
        cell: Tuple[int, int],
    ) -> CellConfiguration:
        """Get the configuration of a cell in a given state.

        Args:
            reference_state (StateInstance): the state that this cell is
                compared against.
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
                action_values_normalised,
                action_values_raw,
                cell,
                self.__cell_entity(reference_state, cell),
            )

        cell_state_id = self.state_pool.get_state_id(cell_state)
        for action in Action:
            action_values_normalised[
                action
            ] = normaliser.get_state_action_value_normalised(cell_state, action)
            action_values_raw[action] = self.agent.get_state_action_value(
                cell_state_id, action
            )

        return CellConfiguration(
            action_values_normalised,
            action_values_raw,
            cell,
            self.__cell_entity(reference_state, cell),
            normaliser.get_state_value_normalised(cell_state),
            self.agent.get_state_value(cell_state_id),
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
