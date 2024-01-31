from collections import defaultdict
from random import choice
from typing import Tuple

import numpy as np

from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.exploration_strategies.base_strategy import (
    BaseExplorationStrategy,
)
from src.model.dynamics.actions import Action


class UpperConfidenceBoundStrategy(BaseExplorationStrategy):
    """This class implements the upper confidence bound strategy.

    Selects the action that has the highest upper confidence bound (potential).

    In the case of ties this strategy selects randomly between the best options.
    """

    initial_action_count = 0
    exploration_bias = 2

    def __init__(self, agent: BaseAgent) -> None:
        """Initialise the Exploration strategy.

        Args:
            agent (BaseAgent): The agent that uses this strategy.
        """
        super().__init__(agent)

        self.state_action_count: defaultdict[
            Tuple[int, Action], int
        ] = defaultdict(lambda: self.initial_action_count)
        self.time_steps = 1

    def upper_confidence_bound(self, state: int, action: Action) -> float:
        """Compute the upper confidence bound for this state action pair.

        Args:
            state (int): the state to consider.
            action (Action): the action to consider with the state.

        Returns:
            float: the upper confidence bound of the value of this state action
                pair.
        """
        q_value = self.agent.get_state_action_value(state, action)
        # divide by zero adjustment
        epsilon = float(np.finfo(float).eps)
        action_count = self.state_action_count[(state, action)] + epsilon
        confidence_bound = np.sqrt(np.log(self.time_steps) / action_count)
        return q_value + confidence_bound * self.exploration_bias

    def select_action(self, state: int) -> Action:
        """Select the action based upon the upper confidence bound strategy.

        this strategy picks the best action based upon the value table weighted
        by a an uncertainty term.

        Args:
            state (int): the state to select the action for.

        Returns:
            Action: the action the agent should select.
        """
        best_action = choice(list(Action))
        best_upper_bound = -float("inf")
        for action in Action:
            upper_bound = self.upper_confidence_bound(state, action)
            if upper_bound > best_upper_bound:
                best_upper_bound = upper_bound
                best_action = action

        self.__increment_state_action_count(state, best_action)
        return best_action

    def __increment_state_action_count(self, state: int, action: Action):
        key = (state, action)
        existing = self.state_action_count[key]
        self.state_action_count[key] = existing + 1
        self.time_steps += 1
