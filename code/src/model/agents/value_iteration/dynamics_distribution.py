from collections import defaultdict
from typing import Any, DefaultDict, Dict, Iterable, List, Set, Tuple

import numpy as np

from ...dynamics.actions import Action
from ...dynamics.base_dynamics import BaseDynamics

# the new state with its expected reward and frequency for getting there
distribution_result = Dict[int, Tuple[float, float]]
observations_type = Dict[int, Dict[int, distribution_result]]


numpy_float = np.ndarray[Any, np.dtype[np.float64]]
numpy_int = np.ndarray[Any, np.dtype[np.int64]]


numpy_distribution_information_type = Tuple[
    numpy_int, numpy_int, numpy_float, numpy_float
]


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
        self.observations: observations_type = {}

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
        """Compile the dynamics state distribution for analysis.

        for some dynamics certain states are not reachable from the initial
        state. if the initial state was changed to be one of these unreachable
        states the distribution would need to be recalculated, and thus the
        value table. The existing value table and distributions could be reused
        but this is not within scope.
        """
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
                current_state_observations[action.value] = distribution
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

    def get_array_representation(
        self,
    ) -> numpy_distribution_information_type:
        """Convert the observations data to an array representation.

        lookup table -> maps a state and action to a range of observations

        the lookup table provides the start and end of a range of observed
        subsequent states.

        next state -> the observed next state
        expected_reward -> the expected reward for transitioning to this state
        frequency -> how often under these state and action do we perform this
        transition

        Returns:
            numpy_distribution_information_type: lookup_table, next_state,
            expected_reward, frequency
        """
        # 3d array state action to index the start and end of the observations
        # states index to ranges in the corresponding arrays

        empty_list_item = [None]

        lookup_table: List[Any] = empty_list_item * len(self.observations)

        next_state: List[Any] = []
        expected_reward: List[Any] = []
        frequency: List[Any] = []

        for state, actions in self.observations.items():
            state_lookup_table: List[Any] = empty_list_item * len(actions)
            for action, observations in actions.items():
                start = len(next_state)
                end = start + len(observations)
                state_lookup_table[action - 1] = [start, end]

                next_state.extend(empty_list_item * len(observations))
                expected_reward.extend(empty_list_item * len(observations))
                frequency.extend(empty_list_item * len(observations))

                for raw_index, observation in enumerate(observations.items()):
                    (
                        next_state_observation,
                        (reward_observation, frequency_observation),
                    ) = observation
                    index = start + raw_index
                    next_state[index] = next_state_observation
                    expected_reward[index] = reward_observation
                    frequency[index] = frequency_observation
            lookup_table[state] = state_lookup_table

        return (
            np.array(lookup_table, dtype=np.int64),
            np.array(next_state, dtype=np.int64),
            np.array(expected_reward, dtype=np.float64),
            np.array(frequency, dtype=np.float64),
        )
