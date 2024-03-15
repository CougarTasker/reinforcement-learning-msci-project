from collections import defaultdict
from math import log, sqrt

import numpy as np

from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.exploration_strategies.base_strategy import (
    BaseExplorationStrategy,
)
from src.model.dynamics.actions import Action
from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.transition_information import TransitionInformation


class UpperConfidenceBoundStrategy(BaseExplorationStrategy):
    """This class implements the upper confidence bound strategy.

    Selects the action that has the highest upper confidence bound (potential).

    In the case of ties this strategy selects randomly between the best options.
    """

    number_of_actions = len(Action)
    initial_action_count = 0
    # divide by zero adjustment
    epsilon = float(np.finfo(float).eps)

    def __init__(self, agent: BaseAgent) -> None:
        """Initialise the Exploration strategy.

        Args:
            agent (BaseAgent): The agent that uses this strategy.
        """
        super().__init__(agent)

        self.state_action_count: defaultdict[int, int] = defaultdict(
            lambda: self.initial_action_count
        )
        self.time_steps = 1
        self.exploration_bias = self.agent.hyper_parameters.get_value(
            HyperParameter.ucb_exploration_bias
        )

    def select_action(self, state: int) -> Action:
        """Select the action based upon the upper confidence bound strategy.

        this strategy picks the best action based upon the value table weighted
        by a an uncertainty term.

        Args:
            state (int): the state to select the action for.

        Returns:
            Action: the action the agent should select.
        """
        get_state_action_value = self.agent.get_state_action_value
        exploration_bias = self.exploration_bias
        state_action_count = self.state_action_count
        epsilon = self.epsilon
        log_time = log(self.time_steps)
        state_index = state * self.number_of_actions

        def ucb(action: Action) -> float:
            q_value = get_state_action_value(state, action)
            action_count = (
                state_action_count[state_index + action.value] + epsilon
            )
            confidence_bound = sqrt(log_time / action_count)
            return q_value + confidence_bound * exploration_bias

        return max(Action, key=ucb)

    def record_transition(self, transition: TransitionInformation) -> None:
        """Use transition information to update internal statics.

        Args:
            transition (TransitionInformation): The transition
                information.

        """
        key = (
            transition.previous_state * self.number_of_actions
            + transition.previous_action.value
        )
        count = self.state_action_count
        count[key] = count[key] + 1
        self.time_steps += 1
