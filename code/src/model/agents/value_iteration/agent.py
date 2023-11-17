import random
from typing import Any, Optional

import numpy as np

from ...dynamics.actions import Action
from ...dynamics.base_dynamics import BaseDynamics
from ..base_agent import BaseAgent
from .dynamics_distribution import DynamicsDistribution, distribution_result

value_table_type = np.ndarray[Any, np.dtype[np.float64]]


class ValueIterationAgent(BaseAgent):
    """Computes the optimal value table for a given dynamics.

    This agent uses that table with the dynamics to pick optimal actions.
    """

    distribution_sample_count = 100
    default_stopping_epsilon = float(np.finfo(float).eps) * 10

    def __init__(
        self,
        discount_rate: float,
        dynamics: BaseDynamics,
        stopping_epsilon: Optional[float] = None,
    ) -> None:
        """Initialise the agent.

        Args:
            discount_rate (float): the rate future rewards should be discounted
            dynamics (BaseDynamics): the dynamics function used to build the
            value table and pick optimal actions
            stopping_epsilon (Optional[float]): the maximum amount of
            inconsistency allowed in the value table, the smaller this value is
            the larger the table will take to converge.
        """
        super().__init__(discount_rate)
        self.dynamics = dynamics
        self.dynamics_distribution = DynamicsDistribution(
            self.distribution_sample_count, dynamics
        )
        self.value_table: Optional[value_table_type] = None
        self.stopping_epsilon: float = (
            stopping_epsilon
            if stopping_epsilon is not None
            else self.default_stopping_epsilon
        )

    def get_value_table(self) -> value_table_type:
        """Get the value table for the provided dynamics.

        If the value table has already been computed it will provide that. if
        not it will compute a new value table, this can be quite costly based
        upon the epsilon, number of states and discount rate.

        Returns:
            value_table_type: the value table for this mdp
        """
        if self.value_table is not None:
            return self.value_table

        if not self.dynamics_distribution.has_compiled():
            self.dynamics_distribution.compile()

        self.value_table = self.compute_value_table()

        return self.value_table

    def compute_value_table(
        self,
    ) -> value_table_type:
        """Compute the optimal value table with value iteration.

        Returns:
            value_table_type: the value table for the dynamics
        """
        state_list = self.dynamics_distribution.list_states()
        value_table = np.random.rand(len(state_list))
        stopping_epsilon = self.stopping_epsilon
        maximum_epsilon: float = 1
        while maximum_epsilon > stopping_epsilon:
            maximum_epsilon = 0
            for state in state_list:
                new_value = self.compute_updated_value(value_table, state)
                epsilon = abs(value_table[state] - new_value)
                value_table[state] = new_value
                maximum_epsilon = max(epsilon, maximum_epsilon)
        return value_table

    def compute_updated_value(
        self,
        value_table: value_table_type,
        state: int,
    ) -> float:
        """Compute the new value of the state based upon the latest value table.

        Args:
            value_table (value_table_type): our current expectation of value in
            future states to base our estimate.
            state (int): the state to calculate the value for.


        Returns:
            float: the new value for this state.
        """
        action_observations = self.dynamics_distribution.observations[state]
        state_value = float(0)
        for action in Action:
            state_value = max(
                state_value,
                self.distribution_value(
                    action_observations[action.value],
                    value_table,
                ),
            )
        return state_value

    def distribution_value(
        self,
        distribution: distribution_result,
        value_table: value_table_type,
    ) -> float:
        """Compute the expected action-value from its distribution.

        Args:
            distribution (distribution_result): the distribution of
            results to weight the rewards
            value_table (value_table_type): our current expectation of value in
            future states to base our estimate.

        Returns:
            float: the expected value for this state and action
        """
        expected_value = 0
        discount_rate = self.discount_rate
        for next_state, (reward, frequency) in distribution.items():
            expected_value += frequency * (
                reward + discount_rate * value_table[next_state]
            )
        return expected_value

    def action_value(self, state: int, action: Action):
        """Compute the expected action-value of a given state.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to get the value of

        Returns:
            float: the expected value for this state and action
        """
        value_table = self.get_value_table()
        return self.distribution_value(
            self.dynamics_distribution.observations[state][action.value],
            value_table,
        )

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        picks the best action based upon the value table.

        Args:
            state (int): the state the agent is performing this action


        Returns:
            Action: the action to take in this state
        """
        best_action = random.choice(list(Action))
        best_value = self.action_value(state, best_action)
        # random default action to help break ties evenly
        for action in Action:
            if action is best_action:
                continue
            action_value = self.action_value(state, action)
            if action_value > best_value:
                best_value = action_value
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

        (not used by this agent)

        Args:
            previous_state (int): the state before the action was taken
            previous_action (Action): the action that was taken.
            new_state (int): The resulting state after the action has been taken
            reward (float): the reward for performing this action

        """
        # not used as the agent learns from the dynamics directly
