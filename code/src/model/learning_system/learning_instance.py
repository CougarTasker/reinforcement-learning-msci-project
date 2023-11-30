from typing import Optional, Tuple

from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.actions import Action
from src.model.dynamics.base_dynamics import BaseDynamics


class LearningInstance(object):
    """An instance of an agent interacting with the environment."""

    def __init__(self, agent: BaseAgent, dynamics: BaseDynamics) -> None:
        """Create the learning instance.

        Args:
            agent (BaseAgent): The agent to learn.
            dynamics (BaseDynamics): The dynamics the agent is learning.
        """
        self.agent = agent
        self.dynamics = dynamics
        self._current_state: Optional[int] = None

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
        self._current_state = next_state
        return (
            last_state,
            action,
            next_state,
            reward,
        )
