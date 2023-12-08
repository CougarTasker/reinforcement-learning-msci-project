from random import choice, random

from ...config.agent_section import AgentConfig
from ...dynamics.actions import Action
from ..base_agent import BaseAgent
from .dynamic_q_table import DynamicQTable
from .reward_replay_queue import RewardReplayQueue


class QLearningAgent(BaseAgent):
    """Agent that learns q-value table to make decisions."""

    replay_queue_length = 100

    def __init__(
        self,
        config: AgentConfig,
    ) -> None:
        """Initialise the agent.

        Args:
            config (AgentConfig): the configuration for the agent.
        """
        super().__init__(config)

        self.table = DynamicQTable(config.learning_rate())
        self.observation_queue = RewardReplayQueue(
            self.table, self.replay_queue_length, config.discount_rate()
        )
        self.exploration_ratio = config.exploration_ratio()

    def get_state_action_value(self, state: int, action: Action) -> float:
        """Get the agents interpretation value of a given state-action.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to get the value of

        Returns:
            float: the expected value for this state and action
        """
        return self.table.get_value(state, action)

    def get_state_value(self, state: int) -> float:
        """Get the agents interpretation of the value of this state.

        Args:
            state (int): the state to evaluate

        Returns:
            float: the agents interpretation of the value of this state
        """
        return self.table.calculate_state_value(state)

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        picks the best action based upon the value table.

        Args:
            state (int): the state the agent is performing this action


        Returns:
            Action: the action to take in this state
        """
        best_action = choice(list(Action))
        if random() < self.exploration_ratio:
            return best_action

        best_action_value = float("-inf")
        for action in Action:
            action_value = self.table.get_value(state, action)
            if action_value > best_action_value:
                best_action_value = action_value
                best_action = action
        return best_action

    def record_transition(
        self,
        previous_state: int,
        previous_action: Action,
        new_state: int,
        reward: float,
    ) -> None:
        """Provide the agent with the information from a transition.

        Args:
            previous_state (int): the state before the action was taken
            previous_action (Action): the action that was taken.
            new_state (int): The resulting state after the action has been taken
            reward (float): the reward for performing this action

        """
        self.observation_queue.add_observation(
            previous_state, previous_action, new_state, reward
        )
