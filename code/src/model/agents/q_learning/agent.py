from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
    HyperParameter,
)

from ...dynamics.actions import Action
from ..base_agent import BaseAgent
from .dynamic_q_table import DynamicQTable
from .exploration_strategies.base_strategy import BaseExplorationStrategy
from .exploration_strategies.epsilon_greedy_strategy import (
    EpsilonGreedyStrategy,
)
from .exploration_strategies.options import ExplorationStrategyOptions
from .exploration_strategies.upper_confidence_bound import (
    UpperConfidenceBoundStrategy,
)
from .reward_replay_queue import RewardReplayQueue


class QLearningAgent(BaseAgent):
    """Agent that learns q-value table to make decisions."""

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

        replay_queue_length = hyper_parameters.get_integer_value(
            HyperParameter.replay_queue_length
        )
        learning_rate = hyper_parameters.get_value(HyperParameter.learning_rate)
        discount_rate = hyper_parameters.get_value(HyperParameter.discount_rate)
        initial_optimism = hyper_parameters.get_value(
            HyperParameter.initial_optimism
        )

        self.strategy = self.set_exploration_strategy(strategy)
        self.table = DynamicQTable(learning_rate, initial_optimism)
        self.observation_queue = RewardReplayQueue(
            self.table, replay_queue_length, discount_rate
        )

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

        Args:
            state (int): the state the agent is performing this action

        Returns:
            Action: the action to take in this state
        """
        return self.strategy.select_action(state)

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
        self.strategy.record_transition(
            previous_state, previous_action, new_state, reward
        )
        self.observation_queue.add_observation(
            previous_state, previous_action, new_state, reward
        )
