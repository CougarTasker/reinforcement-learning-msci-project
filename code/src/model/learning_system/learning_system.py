from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.global_options import GlobalOptions
from src.model.learning_system.learning_instance import LearningInstance
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.model.learning_system.top_entities import TopLevelEntities

from ..agents.q_learning.exploration_strategies.strategy_options import (
    ExplorationStrategyOptions,
)
from .state_description.state_description_factory import StateDescriptionFactory


class LearningSystem(object):
    """Controller for managing one pair of agent and dynamics."""

    def __init__(self) -> None:
        """Class for managing a complete learning system."""
        self.options = GlobalOptions(
            AgentOptions.value_iteration_optimised,
            DynamicsOptions.collection,
            ExplorationStrategyOptions.not_applicable,
            DisplayMode.default,
        )
        self.entities = TopLevelEntities.create_new_entities(self.options)
        self.learning_instance = LearningInstance(self.entities)
        self.state_description_factory = StateDescriptionFactory(self.entities)

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
        self.options = options
        self.entities = self.entities.update_options(options)
        self.learning_instance.update_entities(self.entities)
        self.state_description_factory.update_entities(self.entities)
