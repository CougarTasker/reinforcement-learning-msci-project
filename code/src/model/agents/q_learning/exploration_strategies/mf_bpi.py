from typing import Any, Tuple

import numpy as np

from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.exploration_strategies.base_strategy import (
    BaseExplorationStrategy,
)
from src.model.dynamics.actions import Action
from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.transition_information import TransitionInformation

golden_ratio = (1 + np.sqrt(5)) / 2
golden_ratio_sq = golden_ratio**2


Q_table_type = np.ndarray[Any, np.dtype[np.floating[Any]]]


class MFBPIStrategy(BaseExplorationStrategy):
    """Model Free best policy identification strategy.

    https://openreview.net/forum?id=YEtstXIpP3

    adapted from the authors implementation:
    https://github.com/rssalessio/ModelFreeActiveExplorationRL/blob/main/RiverSwim/agents/mfbpi.py

    """

    float_min = 1e-8
    m_table_learning_rate_factor = 1.1
    action_count = len(Action)
    ensemble_subset_factor = 0.7

    def __init__(self, agent: BaseAgent):
        """Initialise the MFBPI strategy.

        Args:
            agent (BaseAgent): the agent, mostly unused except for the max state
                count
        """
        super().__init__(agent)

        # Initialize parent class with agent parameters
        self.state_count = agent.max_state_count
        self.discount_factor = self.agent.hyper_parameters.get_value(
            HyperParameter.discount_rate
        )
        self.ensemble_size = self.agent.hyper_parameters.get_integer_value(
            HyperParameter.mf_bpi_ensemble_size
        )
        error_sensitivity_parameter = (
            self.agent.hyper_parameters.get_integer_value(
                HyperParameter.mf_error_sensitivity
            )
        )
        self.error_sensitivity: int = 2**error_sensitivity_parameter
        self.exploration_parameter = self.agent.hyper_parameters.get_value(
            HyperParameter.mf_exploration_parameter
        )

        self._state_visits = np.zeros(self.state_count)

        # Initialize a visits matrix for each ensemble member
        self._ensemble_state_action_visits = np.zeros(
            (
                self.ensemble_size,
                self.state_count,
                self.action_count,
                self.state_count,
            )
        )
        # Initialize policy matrix
        self._policy = np.ones(shape=(self.state_count, self.action_count)) / (
            self.action_count
        )

        # Initialize Q-table and M-table for each ensemble member
        # Q -> the understanding of value like normal
        # M -> the amount of uncertainty based on TD errors

        tables = self.q_m_initial_value()
        self._q_table = tables[0]
        self._m_table = tables[1]

    def q_m_initial_value(self) -> Tuple[Q_table_type, Q_table_type]:
        """Get the initial values for the Q and M table.

        Returns:
            Tuple[Q_table_type, Q_table_type]: the initial table values. The
                first table is the Q table and the second is the M table.
        """
        non_discounted_factor = 1 - self.discount_factor
        if self.ensemble_size == 1:
            q_table = (
                np.ones((1, self.state_count, self.action_count))
                / non_discounted_factor
            )
            m_table = np.ones((1, self.state_count, self.action_count)) / (
                non_discounted_factor**self.error_sensitivity
            )
            return q_table, m_table

        q_table = (
            np.tile(
                np.linspace(0, 1, self.ensemble_size)[:, None, None],
                (1, self.state_count, self.action_count),
            )
            / non_discounted_factor
        )
        m_table = np.tile(
            np.linspace(0, 1, self.ensemble_size)[:, None, None],
            (1, self.state_count, self.action_count),
        ) / (non_discounted_factor**self.error_sensitivity)

        q_table = q_table.flatten()
        m_table = m_table.flatten()

        # Shuffle the Q and M matrices
        np.random.shuffle(q_table)
        np.random.shuffle(m_table)

        q_table = q_table.reshape(
            self.ensemble_size, self.state_count, self.action_count
        )
        m_table = m_table.reshape(
            self.ensemble_size, self.state_count, self.action_count
        )
        return q_table, m_table

    def select_action(self, state: int) -> Action:
        """Select the action for this agent to explore.

        Originally called the forwards pass.

        Args:
            state (int): the state the agents action will act upon.

        Returns:
            Action: the action to be chosen.
        """
        forced_exploration_probability = max(
            self.float_min,
            (1 / max(1, self._state_visits[state]))
            ** self.exploration_parameter,
        )
        omega = (1 - forced_exploration_probability) * self._policy[
            state
        ] + forced_exploration_probability * np.ones((self.action_count)) / (
            self.action_count
        )

        action_value = np.random.choice(self.action_count, p=omega)
        return Action(action_value)

    def record_transition(self, experience: TransitionInformation) -> None:
        """Update the exploration strategy's policy with the information.

        Method for backward pass (update agent).

        Args:
            experience (TransitionInformation): the information from a
                transition.
        """
        state, action, reward, new_state = (
            experience.previous_state,
            experience.previous_action.value,
            experience.reward,
            experience.new_state,
        )

        # Increment visit count for the current state pair
        self._state_visits[state] += 1

        # Randomly select a subset of the ensemble
        indexes = np.random.choice(
            self.ensemble_size,
            size=int(self.ensemble_subset_factor * self.ensemble_size),
            replace=False,
        )

        # Update visit counts
        self._ensemble_state_action_visits[
            indexes, state, action, new_state
        ] += 1
        current_visit_count = (
            self._ensemble_state_action_visits[  # noqa: WPS204
                indexes, state, action
            ].sum(-1)
        )
        # visit count horizon exploration vs exploration
        visit_count_horizon = 1 / (1 - self.discount_factor)
        # learning rate for Q-values
        q_learning_rate = (visit_count_horizon + 1) / (
            visit_count_horizon + current_visit_count
        )

        # Compute beta_t
        m_learning_rate = q_learning_rate**self.m_table_learning_rate_factor

        # Calculate target Q value
        target_q_value = reward + self.discount_factor * self._q_table[
            indexes, new_state
        ].max(-1)
        self._q_table[indexes, state, action] = (
            1 - q_learning_rate
        ) * self._q_table[
            indexes, state, action
        ] + q_learning_rate * target_q_value

        # Update M values
        delta = (
            reward
            + self.discount_factor * self._q_table[indexes, new_state].max(-1)
            - self._q_table[indexes, state, action]
        ) / self.discount_factor

        self._m_table[indexes, state, action] = (
            1 - m_learning_rate
        ) * self._m_table[indexes, state, action] + m_learning_rate * (
            delta**self.error_sensitivity
        )

        # Update the ensemble head
        self._head = np.random.choice(self.ensemble_size)

        # Recompute omega values and update the policy
        self.__compute_omega()

    def __compute_omega(self):
        """Compute the omega values.

        which are used to weight different actions in the policy based on their
        estimated value and uncertainty.
        """
        if self.ensemble_size == 1:
            # If there's only one ensemble member, use its Q and M values
            q_values = self._q_table[0]
            m_values = self._m_table[0]
        else:
            # If there are multiple ensemble members, sample a random value from
            # the uniform distribution
            table_quantile = np.random.uniform()
            q_values = np.quantile(self._q_table, table_quantile, axis=0)
            m_values = np.quantile(self._m_table, table_quantile, axis=0)

        # Compute the greedy policy
        greedy_policy = q_values.argmax(1)

        # Identify the suboptimal actions
        subopt_action_indexes = np.array(
            [
                [
                    greedy_policy[state] != action
                    for action in range(self.action_count)
                ]
                for state in range(self.state_count)
            ]
        ).astype(np.bool_)

        # Compute Delta
        delta = np.clip(
            (q_values.max(-1, keepdims=True) - q_values),
            a_min=self.float_min,
            a_max=None,
            out=None,
        )
        delta_subopt = delta[subopt_action_indexes]
        delta_min = delta_subopt.min()

        # Update Delta for optimal actions
        delta[~subopt_action_indexes] = (
            delta_min * (1 - self.discount_factor) / (1 + self.discount_factor)
        )

        # Compute Hsa
        # h_sa = how long the state action should
        # be explored.
        h_sa = (2 + 8 * golden_ratio_sq * m_values) / (delta**2)

        c_value = np.max(
            np.maximum(
                4,
                (4**2)
                * (self.discount_factor**2)
                * golden_ratio_sq
                * m_values[~subopt_action_indexes],
            )
        )

        h_opt = c_value / (delta[~subopt_action_indexes] ** 2)

        # Update Hsa for optimal actions
        h_sa[~subopt_action_indexes] = np.sqrt(
            h_opt * h_sa[subopt_action_indexes].sum() / self.state_count,
        )

        # Compute omega and update policy
        omega = h_sa / h_sa.sum()
        self._policy = omega / omega.sum(-1, keepdims=True)
