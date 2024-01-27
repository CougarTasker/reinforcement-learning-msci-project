from typing_extensions import override

from src.model.learning_system.base_entity_decorator import BaseEntityDecorator
from src.model.learning_system.global_options import GlobalOptions
from src.model.learning_system.top_entities import TopLevelEntities

from ..cell_configuration.cell_configuration_factory import (
    CellConfigurationFactory,
)
from .state_description import StateDescription


class StateDescriptionFactory(BaseEntityDecorator):
    """Factory class for creating state descriptions from states."""

    def __init__(
        self, entities: TopLevelEntities, global_options: GlobalOptions
    ) -> None:
        """Create a state description factory for these entities.

        Args:
            entities (TopLevelEntities): The entities this class uses
                internally.
            global_options (GlobalOptions): The global options for the
                description.
        """
        super().__init__(entities)
        self.cell_configuration_factory = CellConfigurationFactory(entities)
        self.global_options = global_options

    @override
    def update_entities(self, entities: TopLevelEntities) -> None:
        """Update the entities used by this decorator.

        Args:
            entities (TopLevelEntities): the new entities to use.
        """
        super().update_entities(entities)
        self.cell_configuration_factory.update_entities(entities)

    def update_options(self, options: GlobalOptions):
        """Update the options used in the state descriptions.

        Args:
            options (GlobalOptions): the new options.
        """
        self.global_options = options

    def create_state_description(self, state_id: int) -> StateDescription:
        """Create a new state description from a given state ID.

        Args:
            state_id (int): the state to describe for the UI.

        Returns:
            StateDescription: All of the details of the state for the UI.
        """
        return StateDescription(
            self.grid_world,
            self.state_pool.get_state_from_id(state_id),
            self.cell_configuration_factory.get_cell_configuration(state_id),
            self.global_options,
        )
