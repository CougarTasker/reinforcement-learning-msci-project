from typing import Optional

from typing_extensions import override

from src.model.learning_system.base_entity_decorator import BaseEntityDecorator
from src.model.learning_system.top_level_entities.container import (
    EntityContainer,
)
from src.model.transition_information import TransitionInformation


class LearningInstance(BaseEntityDecorator):
    """An instance of an agent interacting with the environment."""

    def __init__(self, entities: EntityContainer) -> None:
        """Create the learning instance.

        Args:
            entities (EntityContainer): the top level entities used in this
                learning instance.
        """
        super().__init__(entities)
        self._current_state: Optional[int] = None

    @override
    def update_entities(self, entities: EntityContainer) -> None:
        """Update the entities used by this decorator.

        Args:
            entities (EntityContainer): the new entities to use.
        """
        different_agent = self.entities.agent is not entities.agent
        different_dynamics = self.entities.dynamics is not entities.dynamics
        if different_agent or different_dynamics:
            self._current_state = None
        super().update_entities(entities)

    def get_current_state(self) -> int:
        """Get the current state ID.

        Returns:
            int: the current state ID
        """
        if self._current_state is not None:
            return self._current_state
        self._current_state = self.dynamics.initial_state_id()
        return self._current_state

    def reset_state(self) -> int:
        """Reset the current state to the initial state.

        Returns:
            int: the initial state id
        """
        self._current_state = self.dynamics.initial_state_id()
        return self._current_state

    def perform_action(
        self,
    ) -> TransitionInformation:
        """Perform one action chosen by the agent.

        Returns:
            TransitionInformation: the transition information, the last
            state, the action chosen, the next state, the reward received for
            this action.
        """
        last_state = self.get_current_state()
        agent = self.agent
        action = agent.evaluate_policy(last_state)
        next_state, reward = self.dynamics.next_state_id(last_state, action)

        transition = TransitionInformation(
            last_state, action, next_state, reward
        )
        agent.record_transition(transition)
        self.statistics.record_transition(transition)
        self._current_state = next_state
        return transition
