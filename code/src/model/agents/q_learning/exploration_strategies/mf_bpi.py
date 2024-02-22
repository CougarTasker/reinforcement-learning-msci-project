# flake8: noqa
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


class MFBPIStrategy(BaseExplorationStrategy):
    """Model Free best policy identification strategy.

    https://openreview.net/forum?id=YEtstXIpP3

    adapted from the authors implementation:
    https://github.com/rssalessio/ModelFreeActiveExplorationRL/blob/main/RiverSwim/agents/mfbpi.py

    """

    suggested_exploration_parameter = 1
    dim_action_space = len(Action)

    def __init__(self, agent: BaseAgent):
        """Initialise the MFBPI strategy.

        Args:
            agent (BaseAgent): the agent, mostly unused except for the max state
                count
        """
        super().__init__(agent)

        # Initialize parent class with agent parameters
        self.dim_state_space = agent.max_state_count
        self.discount_factor = self.agent.hyper_parameters.get_value(
            HyperParameter.discount_rate
        )
        self.ensemble_size = self.agent.hyper_parameters.get_integer_value(
            HyperParameter.mf_bpi_ensemble_size
        )

        self.kbar = self.agent.hyper_parameters.get_integer_value(
            HyperParameter.mf_bpi_kbar
        )

        self.exp_visits = np.zeros((self.ns, self.na, self.ns))
        self.state_action_visits = np.zeros((self.ns, self.na))
        self.total_state_visits = np.zeros((self.ns))
        self.greedy_policy = np.zeros((self.ns), dtype=np.int64)
        self.omega = np.ones((self.ns, self.na))
        self.exploration_parameter = self.suggested_exploration_parameter

        # Create a uniform policy matrix
        self.uniform_policy = np.ones((self.ns, self.na)) / (self.ns * self.na)

        # Initialize Q_greedy matrix
        self.Q_greedy = (
            np.ones((self.ns, self.na))
            / (self.ns * self.na)
            / (1 - self.discount_factor)
        )

        # Initialize Q-table and M-table for each ensemble member
        if self.ensemble_size > 1:
            self.Q = np.tile(
                np.linspace(0, 1, self.ensemble_size)[:, None, None],
                (1, self.ns, self.na),
            ) / (1 - self.discount_factor)
            self.M = np.tile(
                np.linspace(0, 1, self.ensemble_size)[:, None, None],
                (1, self.ns, self.na),
            ) / ((1 - self.discount_factor) ** (2**self.kbar))

            self.Q = self.Q.flatten()
            self.M = self.M.flatten()

            # Shuffle the Q and M matrices
            np.random.shuffle(self.Q)
            np.random.shuffle(self.M)
            self.Q = self.Q.reshape(self.ensemble_size, self.ns, self.na)
            self.M = self.M.reshape(self.ensemble_size, self.ns, self.na)
        else:
            self.Q = np.ones((1, self.ns, self.na)) / (1 - self.discount_factor)
            self.M = np.ones((1, self.ns, self.na)) / (
                (1 - self.discount_factor) ** (2**self.kbar)
            )

        # Initialize omega and policy matrices
        self.omega = np.ones(shape=(self.ns, self.na)) / (self.ns * self.na)
        self.policy = np.ones(shape=(self.ns, self.na)) / (self.na)

        # Initialize a visits matrix for each ensemble member
        self._visits = np.zeros((self.ensemble_size, self.ns, self.na, self.ns))

    @property
    def ns(self) -> int:
        """Shorthand property for the number of states.

        Returns:
            int: the maximum number of states.
        """
        return self.dim_state_space

    @property
    def na(self) -> int:
        """Shorthand property for the number of actions.

        Returns:
            int: The number of actions.
        """
        return self.dim_action_space

    def forced_exploration_callable(
        self, state: int, minimum_exploration: float = 0.1
    ) -> float:
        """Compute the forced exploration probability.

        Args:
            state (int): The state that we are exploring from.
            minimum_exploration (float): the minimal amount of
                exploration. Defaults to 0.1.

        Returns:
            float: forced exploration probability.
        """
        return max(
            minimum_exploration,
            (1 / max(1, self.total_state_visits[state]))
            ** self.exploration_parameter,
        )

    def select_action(self, state: int) -> Action:
        """Select the action for this agent to explore.

        Originally called the forwards pass.

        Args:
            state (int): the state the agents action will act upon.

        Returns:
            Action: the action to be chosen.
        """
        epsilon = self.forced_exploration_callable(
            state, minimum_exploration=1e-3
        )
        omega = (1 - epsilon) * self.policy[state] + epsilon * np.ones(
            (self.na)
        ) / (self.na)

        action_value = np.random.choice(self.na, p=omega)
        return Action(action_value)

    def record_transition(self, experience: TransitionInformation) -> None:
        """Update the exploration strategy's policy with the information.

        Method for backward pass (update agent).

        Args:
            experience (TransitionInformation): the information from a
                transition.
        """
        # Increment visit count for the current state-action pair
        self.exp_visits[
            experience.previous_state,
            experience.previous_action.value,
            experience.new_state,
        ] += 1
        self.state_action_visits[
            experience.previous_state, experience.previous_action.value
        ] += 1

        # Update last visit time and total state visits count for the next state

        self.total_state_visits[experience.new_state] += 1

        # If this is the first time step, update last visit time and total
        # state visits count for the current state
        if self.total_state_visits[experience.previous_state] == 0:
            self.total_state_visits[experience.previous_state] = 1

        # Process the experience to update the agent's internal model
        self.__process_experience(experience)

    def __process_experience(self, experience: TransitionInformation) -> None:
        # Unpack the experience tuple
        s, a, r, sp = (
            experience.previous_state,
            experience.previous_action.value,
            experience.reward,
            experience.new_state,
        )

        # Randomly select a subset of the ensemble
        idxs = np.random.choice(
            self.ensemble_size,
            size=int(0.7 * self.ensemble_size),
            replace=False,
        )

        # Update visit counts
        self._visits[idxs, s, a, sp] += 1
        k = self._visits[idxs, s, a].sum(-1)
        H = 1 / (1 - self.discount_factor)
        alpha_t = (H + 1) / (H + k)

        # Compute beta_t
        beta_t = alpha_t**1.1

        # Calculate target Q value
        target = r + self.discount_factor * self.Q[idxs, sp].max(-1)
        self.Q[idxs, s, a] = (1 - alpha_t) * self.Q[
            idxs, s, a
        ] + alpha_t * target

        # Update Q_greedy
        k = self.exp_visits[s, a].sum()
        alpha_t = (H + 1) / (H + k)
        target = r + self.discount_factor * self.Q_greedy[sp].max(-1)
        self.Q_greedy[s, a] = (1 - alpha_t) * self.Q_greedy[
            s, a
        ] + alpha_t * target

        # Update M values
        delta = (
            r
            + self.discount_factor * self.Q[idxs, sp].max(-1)
            - self.Q[idxs, s, a]
        ) / self.discount_factor
        self.M[idxs, s, a] = (1 - beta_t) * self.M[idxs, s, a] + beta_t * (
            delta ** (2**self.kbar)
        )

        # Update the greedy policy
        self.greedy_policy = (
            np.random.random(self.Q_greedy.shape)
            * (self.Q_greedy == self.Q_greedy.max(-1, keepdims=True))
        ).argmax(-1)

        # Update the ensemble head
        self._head = np.random.choice(self.ensemble_size)

        # Recompute omega values and update the policy
        self.__compute_omega()

    def __compute_omega(self):
        # If there's only one ensemble member, use its Q and M values
        if self.ensemble_size == 1:
            q_values = self.Q[0]
            m_values = self.M[0]
        else:
            # If there are multiple ensemble members, sample a random value from
            # the uniform distribution
            x = np.random.uniform()
            q_values = np.quantile(self.Q, x, axis=0)
            m_values = np.quantile(self.M, x, axis=0)

        # Compute the greedy policy
        greedy_policy = q_values.argmax(1)

        # Identify the suboptimal actions
        idxs_subopt_actions = np.array(
            [
                [
                    False if greedy_policy[s] == a else True
                    for a in range(self.na)
                ]
                for s in range(self.ns)
            ]
        ).astype(np.bool_)

        # Compute Delta
        delta = np.clip(
            (q_values.max(-1, keepdims=True) - q_values), a_min=1e-8, a_max=None
        )
        delta_subopt = delta[idxs_subopt_actions]
        delta_min = delta_subopt.min()

        # Update Delta for optimal actions
        delta[~idxs_subopt_actions] = (
            delta_min * (1 - self.discount_factor) / (1 + self.discount_factor)
        )

        # Compute Hsa
        h_sa = (2 + 8 * golden_ratio_sq * m_values) / (delta**2)

        c_value = np.max(
            np.maximum(
                4,
                16
                * (self.discount_factor**2)
                * golden_ratio_sq
                * m_values[~idxs_subopt_actions],
            )
        )

        h_opt = c_value / (delta[~idxs_subopt_actions] ** 2)

        # Update Hsa for optimal actions
        h_sa[~idxs_subopt_actions] = np.sqrt(
            h_opt * h_sa[idxs_subopt_actions].sum() / self.ns,
        )

        # Compute omega and update policy
        self.omega = h_sa / h_sa.sum()
        self.policy = self.omega / self.omega.sum(-1, keepdims=True)
