from collections import defaultdict
from typing import Dict, List

from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
    HyperParameter,
)
from src.model.transition_information import TransitionInformation

from ...dynamics.actions import Action
from ..base_agent import BaseAgent
from .exploration_strategies.base_strategy import BaseExplorationStrategy
from .exploration_strategies.epsilon_greedy_strategy import (
    EpsilonGreedyStrategy,
)
from .exploration_strategies.options import ExplorationStrategyOptions
from .exploration_strategies.upper_confidence_bound import (
    UpperConfidenceBoundStrategy,
)


class QLearningAgent(BaseAgent):
    """Agent that learns q-value table to make decisions."""

    action_count = len(Action)

    def __init__(
        self,
        hyper_parameters: BaseHyperParameterStrategy,
        strategy: ExplorationStrategyOptions,
    ) -> None:
        """Initialise the agent.

        Args:
            hyper_parameters (BaseHyperParameterStrategy): the hyper parameters
                the agent should use.
            strategy (ExplorationStrategyOptions): The strategy the agent should
                use to select actions.
        """
        super().__init__(hyper_parameters)

        self.max_queue_length = hyper_parameters.get_integer_value(
            HyperParameter.replay_queue_length
        )
        self.learning_rate = hyper_parameters.get_value(
            HyperParameter.learning_rate
        )
        self.discount_rate = hyper_parameters.get_value(
            HyperParameter.discount_rate
        )
        initial_optimism = hyper_parameters.get_value(
            HyperParameter.initial_optimism
        )
        self.queue: List[TransitionInformation] = []
        self.table: Dict[int, float] = defaultdict(lambda: initial_optimism)
        self.strategy = self.set_exploration_strategy(strategy)

    def set_exploration_strategy(
        self, strategy: ExplorationStrategyOptions
    ) -> BaseExplorationStrategy:
        """Set the current strategy used by the agent.

        Args:
            strategy (ExplorationStrategyOptions): specifies the strategy to
                use.

        Raises:
            ValueError: if an invalid strategy is provided

        Returns:
            BaseExplorationStrategy: the new strategy the agent will use.
        """
        match strategy:
            case ExplorationStrategyOptions.epsilon_greedy:
                self.strategy = EpsilonGreedyStrategy(self)

            case ExplorationStrategyOptions.upper_confidence_bound:
                self.strategy = UpperConfidenceBoundStrategy(self)
            case _:
                raise ValueError(f"Unknown strategy provided {strategy}")

        return self.strategy

    def get_state_action_value(self, state: int, action: Action) -> float:
        """Get the agents interpretation value of a given state-action.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to get the value of

        Returns:
            float: the expected value for this state and action
        """
        return self.table[state * self.action_count + action.value]

    def get_state_value(self, state: int) -> float:
        """Get the agents interpretation of the value of this state.

        Args:
            state (int): the state to evaluate

        Returns:
            float: the agents interpretation of the value of this state
        """
        table = self.table
        action_count = self.action_count
        state_index = state * action_count
        return max(
            table[state_index + offset] for offset in range(action_count)
        )

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        Args:
            state (int): the state the agent is performing this action

        Returns:
            Action: the action to take in this state
        """
        return self.strategy.select_action(state)

    def record_transition(self, transition: TransitionInformation) -> None:
        """Provide the agent with the information from a transition.

        Args:
            transition (TransitionInformation): The transition information.

        """
        self.strategy.record_transition(transition)

        table = self.table
        learning_rate = self.learning_rate
        queue = self.queue
        table = self.table
        discount_rate = self.discount_rate
        action_count = self.action_count

        queue.insert(0, transition)
        if len(queue) > self.max_queue_length:
            queue.pop()

        for obs in queue:
            new_state_index = obs.new_state * action_count
            new_state_value = max(
                table[new_state_index + index] for index in range(action_count)
            )

            observed_value = obs.reward + discount_rate * new_state_value
            index = (
                obs.previous_state * action_count + obs.previous_action.value
            )

            existing_value = table[index]
            table[index] = existing_value + learning_rate * (
                observed_value - existing_value
            )
