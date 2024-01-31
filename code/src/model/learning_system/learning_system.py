from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.global_options import (
    GlobalOptions,
    TopEntitiesOptions,
)
from src.model.learning_system.learning_instance.learning_instance import (
    LearningInstance,
)
from src.model.learning_system.options import (
    AgentOptions,
    AutomaticOptions,
    DynamicsOptions,
)
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.model.learning_system.top_entities import TopEntitiesCache

from ..agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from .state_description.state_description_factory import StateDescriptionFactory


class LearningSystem(object):
    """Controller for managing one pair of agent and dynamics."""

    def __init__(self) -> None:
        """Class for managing a complete learning system."""
        top_level_options = TopEntitiesOptions(
            AgentOptions.value_iteration_optimised,
            DynamicsOptions.collection,
            ExplorationStrategyOptions.not_applicable,
        )
        self.options = GlobalOptions(
            top_level_options,
            DisplayMode.default,
            AutomaticOptions.manual,
        )
        self.entity_cache = TopEntitiesCache()
        self.entities = self.entity_cache.get_entities(top_level_options)
        self.learning_instance = LearningInstance(self.entities)
        self.state_description_factory = StateDescriptionFactory(
            self.entities, self.options
        )

    def get_current_state(self) -> StateDescription:
        """Get the current state of the learning instance.

        Returns:
            StateDescription: the current configuration for this state.
        """
        state_id = self.learning_instance.get_current_state()
        return self.state_description_factory.create_state_description(state_id)

    def update_options(self, options: GlobalOptions):
        """Set the global options used by this system.

        Args:
            options (GlobalOptions): how to display the learning instance
        """
        entity_options = options.top_level_options
        entities_updated = entity_options != self.options.top_level_options
        self.options = options
        self.state_description_factory.update_options(options)
        if entities_updated:
            self.entities = self.entity_cache.get_entities(entity_options)
            self.learning_instance.update_entities(self.entities)
            self.state_description_factory.update_entities(self.entities)

    def reset_top_level(self):
        """Reset the toplevel entities. wipes all learning information."""
        self.entities = self.entity_cache.create_new_entities(
            self.options.top_level_options
        )
        self.learning_instance.update_entities(self.entities)
        self.state_description_factory.update_entities(self.entities)
