from typing import Optional, Tuple

from typing_extensions import override

from src.model.dynamics.actions import Action
from src.model.learning_system.base_entity_decorator import BaseEntityDecorator
from src.model.learning_system.top_entities import TopLevelEntities


class LearningInstance(BaseEntityDecorator):
    """An instance of an agent interacting with the environment."""

    def __init__(self, entities: TopLevelEntities) -> None:
        """Create the learning instance.

        Args:
            entities (TopLevelEntities): the top level entities used in this
                learning instance.
        """
        super().__init__(entities)
        self._current_state: Optional[int] = None

    @override
    def update_entities(self, entities: TopLevelEntities) -> None:
        """Update the entities used by this decorator.

        Args:
            entities (TopLevelEntities): the new entities to use.
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
    ) -> Tuple[int, Action, int, float]:
        """Perform one action chosen by the agent.

        Returns:
            Tuple[int, Action, int, float]: the transition information, the last
            state, the action chosen, the next state, the reward received for
            this action.
        """
        last_state = self.get_current_state()

        action = self.agent.evaluate_policy(last_state)
        next_state, reward = self.dynamics.next_state_id(last_state, action)
        self.agent.record_transition(last_state, action, next_state, reward)
        self.statistics.record_transition(
            last_state, action, next_state, reward
        )
        self._current_state = next_state
        return (
            last_state,
            action,
            next_state,
            reward,
        )
