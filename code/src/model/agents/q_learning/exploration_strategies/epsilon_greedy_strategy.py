from random import choice, random

from src.model.agents.q_learning.exploration_strategies.base_strategy import (
    BaseExplorationStrategy,
)
from src.model.dynamics.actions import Action


class EpsilonGreedyStrategy(BaseExplorationStrategy):
    """This class implements the epsilon greedy strategy.

    Selects the agents current understanding of what the best action is with a
    fixed probability of exploring. to explore the agent picks any action at
    random.

    In the case of ties this strategy selects randomly between the best options.
    """

    def select_action(self, state: int) -> Action:
        """Select the action based upon the epsilon greedy strategy.

        this strategy picks the best action based upon the value table with a
        given chance of selecting any action.

        Args:
            state (int): the state to select the action for.

        Returns:
            Action: the action the agent should select.
        """
        best_action = choice(list(Action))
        if random() < self.config.exploration_ratio():
            return best_action

        best_action_value = -float("inf")
        for action in Action:
            action_value = self.agent.get_state_action_value(state, action)
            if action_value > best_action_value:
                best_action_value = action_value
                best_action = action
        return best_action
