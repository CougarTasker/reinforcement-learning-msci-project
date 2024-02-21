from random import choice, random
from typing import Any

import numpy as np

from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.exploration_strategies.base_strategy import (
    BaseExplorationStrategy,
)
from src.model.dynamics.actions import Action
from src.model.hyperparameters.base_parameter_strategy import HyperParameter


class EpsilonGreedyStrategy(BaseExplorationStrategy):
    """This class implements the epsilon greedy strategy.

    Selects the agents current understanding of what the best action is with a
    fixed probability of exploring. to explore the agent picks any action at
    random.

    In the case of ties this strategy selects randomly between the best options.
    """

    min_safe_exploration_ratio = float(np.finfo(float).eps) * 100

    def __init__(self, agent: BaseAgent) -> None:
        """Initialise the Epsilon greedy strategy.

        Args:
            agent (BaseAgent): The agent using this strategy
        """
        super().__init__(agent)
        self.exploration_ratio = agent.hyper_parameters.get_value(
            HyperParameter.eg_initial_exploration_ratio
        )
        self.decay_rate = agent.hyper_parameters.get_value(
            HyperParameter.eg_decay_rate
        )

    def select_action(self, state: int) -> Action:
        """Select the action based upon the epsilon greedy strategy.

        this strategy picks the best action based upon the value table with a
        given chance of selecting any action.

        Args:
            state (int): the state to select the action for.

        Returns:
            Action: the action the agent should select.
        """
        if random() < self.exploration_ratio:
            return choice(list(Action))

        state_action_value = self.agent.get_state_action_value

        def key(action: Action) -> float:
            return state_action_value(state, action)

        return max(Action, key=key)

    def record_transition(self, *args: Any) -> None:
        """Record that a transition has taken place.

        this is used by this strategy to discount its parameter.

        Args:
            args (Any): not used.
        """
        self.exploration_ratio = max(
            self.exploration_ratio * self.decay_rate,
            self.min_safe_exploration_ratio,
        )
