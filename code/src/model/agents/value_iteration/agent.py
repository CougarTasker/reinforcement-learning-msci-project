from typing import Any, Optional

import numpy as np

from ...dynamics.actions import Action
from ...dynamics.base_dynamics import BaseDynamics
from ..base_agent import BaseAgent
from .dynamics_distribution import DynamicsDistribution

value_table_type = np.ndarray[Any, np.dtype[np.float64]]


class ValueIterationAgent(BaseAgent):
    """Computes the optimal value table for a given dynamics.

    This agent uses that table with the dynamics to pick optimal actions.
    """

    distribution_sample_count = 100
    stopping_epsilon = float(np.finfo(float).eps) * 10

    def __init__(self, discount_rate: float, dynamics: BaseDynamics) -> None:
        """Initialise the agent.

        Args:
            discount_rate (float): the rate future rewards should be discounted
            by.
            dynamics (BaseDynamics): the dynamics function used to build the
            value table and pick optimal actions
        """
        super().__init__(discount_rate)
        self.dynamics = dynamics
        self.dynamics_distribution = DynamicsDistribution(
            self.distribution_sample_count, dynamics
        )
        self.value_table: Optional[value_table_type] = None

    def compute_updated_value(self, state: int) -> float:
        """Compute the new value of the state based upon the latest value table.

        Args:
            state (int): the state to get the value for

        Raises:
            RuntimeError: if the value_table has not been populated.

        Returns:
            float: the new value for this state.
        """
        state_observations = self.dynamics_distribution.observations[state]
        if self.value_table is None:
            raise RuntimeError()
        state_value = 0
        for action in Action:
            resulting_states = state_observations[action]
            state_action_value = 0
            for next_state, (reward, frequency) in resulting_states.items():
                state_action_value += frequency * (
                    reward + self.discount_rate * self.value_table[next_state]
                )
            state_value = max(state_value, state_action_value)
        return state_value

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

        self.value_table = np.random.rand(
            self.dynamics_distribution.get_state_count()
        )

        state_list = self.dynamics_distribution.list_states()

        maximum_epsilon: float = self.stopping_epsilon + 1
        while maximum_epsilon > self.stopping_epsilon:
            maximum_epsilon = 0
            for state in state_list:
                new_value = self.compute_updated_value(state)
                epsilon = abs(self.value_table[state] - new_value)
                self.value_table[state] = new_value
                maximum_epsilon = max(epsilon, maximum_epsilon)

        return self.value_table

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        Args:
            state (int): the state the agent is performing this action

        Raises:
            NotImplementedError: If this method has not been overridden by
            concrete agent.

        Should return:
            Action: the action to take in this state
        """
        raise NotImplementedError()

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
