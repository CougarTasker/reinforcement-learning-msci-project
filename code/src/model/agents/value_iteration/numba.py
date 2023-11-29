import numpy as np
from numba import jit

from .dynamics_distribution import numpy_float, numpy_int
from .types import value_table_type


@jit(nopython=True, cache=True, fastmath=True)
def compute_value_table(  # noqa: WPS211
    discount_rate: float,
    stopping_epsilon: float,
    lookup_table: numpy_int,
    next_state: numpy_int,
    expected_reward: numpy_float,
    frequency: numpy_float,
) -> value_table_type:
    """Compute the optimal value table with value iteration.

    Args:
        discount_rate (float): The rate to discount future rewards
        stopping_epsilon (float): The error amount that is acceptable.
        lookup_table (numpy_int): maps state and actions to observed transitions
        next_state (numpy_int): the following state after some state and action
        expected_reward (numpy_float): the average reward after completing some
        action.
        frequency (numpy_float): The relative frequency of this transition
        compared to others under the same initial state and action.

    Returns:
        value_table_type: the value table for the dynamics
    """
    number_of_states = lookup_table.shape[0]
    value_table = np.random.rand(number_of_states)
    maximum_epsilon: float = 1
    while maximum_epsilon > stopping_epsilon:
        maximum_epsilon = 0
        for state in range(number_of_states):
            new_value = compute_updated_value(
                value_table,
                state,
                discount_rate,
                lookup_table,
                next_state,
                expected_reward,
                frequency,
            )
            epsilon = abs(value_table[state] - new_value)
            value_table[state] = new_value
            maximum_epsilon = max(epsilon, maximum_epsilon)
    return value_table


@jit(nopython=True, cache=True, fastmath=True)
def compute_updated_value(  # noqa: WPS211
    value_table: value_table_type,
    state: int,
    discount_rate: float,
    lookup_table: numpy_int,
    next_state: numpy_int,
    expected_reward: numpy_float,
    frequency: numpy_float,
) -> float:
    """Compute the new value of the state based upon the latest value table.

    Args:
        value_table (value_table_type): our current expectation of value in
        future states to base our estimate.
        state (int): the state to calculate the value for.
        discount_rate (float): The rate to discount future rewards
        lookup_table (numpy_int): maps state and actions to observed transitions
        next_state (numpy_int): the following state after some state and action
        expected_reward (numpy_float): the average reward after completing some
        action.
        frequency (numpy_float): The relative frequency of this transition
        compared to others under the same initial state and action.


    Returns:
        float: the new value for this state.
    """
    state_value = float(0)
    for observation_range in lookup_table[state]:
        start = observation_range[0]
        end = observation_range[1]

        subsequent_values = discount_rate * value_table[next_state[start:end]]
        weighted_rewards = frequency[start:end] * (
            expected_reward[start:end] + subsequent_values
        )

        state_value = max(state_value, weighted_rewards.mean())
    return state_value
