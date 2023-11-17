from collections import defaultdict
from typing import Any, DefaultDict, Dict, Iterable, List, Set, Tuple

import numpy as np

from ...dynamics.actions import Action
from ...dynamics.base_dynamics import BaseDynamics

# the new state with its expected reward and frequency for getting there
distribution_result = Dict[int, Tuple[float, float]]


class DynamicsDistribution(object):
    """Calculates a dynamics distribution."""

    def __init__(
        self, per_state_sample_count: int, dynamics: BaseDynamics
    ) -> None:
        """Initialise the dynamics distribution.

        Args:
            per_state_sample_count (int): the number of samples to collect from
            each state, for deterministic dynamics only one is needed.
            dynamics (BaseDynamics): the dynamics to get the distribution for.
        """
        self.sample_count = (
            per_state_sample_count if dynamics.is_stochastic() else 1
        )
        self.dynamics = dynamics

        # state, action, new_state -> reward, freq
        self.observations: Dict[int, Dict[Action, distribution_result]] = {}

    def compute_state_action_distribution(
        self, state: int, action: Action
    ) -> distribution_result:
        """Compute the subsequent distribution for a given action and state.

        Args:
            state (int): the state to to get the distribution for.
            action (Action): the action to get the distribution for.

        Returns:
            distribution_result: the distribution of states and their
            expected immediate rewards.
        """
        observed_states: DefaultDict[int, List[float]] = defaultdict(list)

        for _iteration in range(self.sample_count):  # noqa: WPS122
            next_id, reward = self.dynamics.next_state_id(state, action)
            observed_states[next_id].append(reward)

        reduced_output: distribution_result = {}
        for new_state, observations in observed_states.items():
            frequency = len(observations) / self.sample_count
            average_reward = np.array(observations).mean()
            reduced_output[new_state] = (average_reward, frequency)
        return reduced_output

    def compile(self):
        """Compile the dynamics state distribution for analysis."""
        frontier: List[int] = [self.dynamics.initial_state_id()]
        seen_states: Set[int] = set(frontier)

        seen_add = seen_states.add  # performance tweak
        frontier_add = frontier.append

        def add_states(states: Iterable[int]):
            for state in states:
                if state not in seen_states:
                    seen_add(state)
                    frontier_add(state)

        while frontier:
            current_state = frontier.pop(0)
            current_state_observations = {}
            self.observations[current_state] = current_state_observations
            for action in Action:
                distribution = self.compute_state_action_distribution(
                    current_state, action
                )
                current_state_observations[action] = distribution
                add_states(distribution.keys())

    def has_compiled(self) -> bool:
        """Check weather the observations have been compiled yet.

        Returns:
            bool: true when the distribution has been compiled.
        """
        return bool(self.observations)

    def check_compiled(self) -> None:
        """Throw error if not compiled yet.

        Raises:
            RuntimeError: Thrown if the class has not compiled the observations.
        """
        if not self.has_compiled():
            raise RuntimeError("not yet compiled")

    def get_state_count(self) -> int:
        """Get the number of states in the MDP.

        Returns:
            int: the number of states
        """
        self.check_compiled()
        return len(self.observations)

    def list_states(self) -> np.ndarray[Any, np.dtype[np.integer]]:
        """Get array of all the states.

        Returns:
            np.ndarray[Any, np.dtype[np.integer]]: all possible states as an
            array.
        """
        return np.array(list(self.observations.keys()))
