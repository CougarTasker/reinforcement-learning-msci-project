from ..dynamics.test_collection_dynamics import dynamics
from src.model.dynamics.collection_dynamics import CollectionDynamics
from src.model.agents.value_iteration.agent import ValueIterationAgent
from src.model.agents.value_iteration.dynamics_distribution import (
    DynamicsDistribution,
)
from numpy import testing
import numpy as np

from typing import Set

# These values are calculated based upon the collection dynamics as visualised
# in the graphvis.svg. these dynamics were produced on the fixed test 3x3 grid


def find_final_states(dd: DynamicsDistribution):
    final_states = []
    for state, subsequent_states in dd.observations.items():
        next_states = set()
        for states_distributions in subsequent_states.values():
            for next_state in states_distributions.keys():
                next_states.add(next_state)
        if state in next_states and len(next_states) == 1:
            final_states.append(state)
    return final_states


def find_immediately_adjacent(agent: ValueIterationAgent, target_state: int):
    """Find the states that will lead to this state but could not get a higher
    value through another action, not including the current state"""
    adjacent_cells = set()
    observations = agent.dynamics_distribution.observations
    value_table = agent.get_value_table()

    for (
        current_state,
        subsequent_states,
    ) in observations.items():
        if current_state in adjacent_cells:
            break
        for states_distributions in subsequent_states.values():
            if current_state in adjacent_cells:
                break
            for next_state in states_distributions.keys():
                if next_state == target_state:
                    adjacent_cells.add(current_state)
                    break

    # remove current states
    if target_state in adjacent_cells:
        adjacent_cells.remove(target_state)

    # filter adjacent cells not under the influence of the target state
    # assumes deterministic agent
    non_influenced_states = set()
    for current_state in adjacent_cells:
        target_state_value = 0
        for state_distribution in observations[current_state].values():
            for next_state, (
                average_reward,
                frequency,
            ) in state_distribution.items():
                if next_state == target_state and average_reward == 0:
                    target_state_value = (
                        agent.discount_rate * value_table[target_state]
                        + average_reward
                    )

        for state_distribution in observations[current_state].values():
            for next_state, (
                average_reward,
                _frequency,
            ) in state_distribution.items():
                expected_value = (
                    agent.discount_rate * value_table[next_state]
                    + average_reward
                )
                if (
                    next_state != target_state
                    and expected_value > target_state_value
                ):
                    non_influenced_states.add(current_state)
    for state in non_influenced_states:
        adjacent_cells.remove(state)
    return adjacent_cells


def find_all_adjacent(agent: ValueIterationAgent, target_states: list[int]):
    adjacent = set()
    for target_state in target_states:
        adjacent.update(find_immediately_adjacent(agent, target_state))
    return list(adjacent)


def find_reward_and_discount_adjacent(agent: ValueIterationAgent):
    observations = agent.dynamics_distribution.observations
    table = agent.get_value_table()
    discount_and_reward_adjacent = []
    for state, subsequent_states in observations.items():
        valuable_reward_state = None
        valuable_reward_state_value = 0
        for state_distribution in subsequent_states.values():
            for next_state, (
                average_reward,
                _frequency,
            ) in state_distribution.items():
                if average_reward == 1 and table[next_state] > 0.0001:
                    valuable_reward_state = next_state
                    valuable_reward_state_value = (
                        table[next_state] * agent.discount_rate + 1
                    )
        if valuable_reward_state is None:
            continue
        for state_distribution in subsequent_states.values():
            for next_state, (
                average_reward,
                _frequency,
            ) in state_distribution.items():
                reward = (
                    table[next_state] * agent.discount_rate + average_reward
                )
                if reward > valuable_reward_state_value:
                    break
        discount_and_reward_adjacent.append(state)

    return discount_and_reward_adjacent


def test_get_table(dynamics: CollectionDynamics):
    discount_rate = 0.9
    agent = ValueIterationAgent(discount_rate, dynamics)
    difference_digits = -np.log10(agent.stopping_epsilon) - 1
    table = agent.get_value_table()

    final_states = find_final_states(agent.dynamics_distribution)  # 22, 17
    # final states should have no value as they are accumulate and provide no
    # more reward
    testing.assert_almost_equal(
        table[final_states], np.zeros(len(final_states)), difference_digits
    )

    # values adjacent to the final state should have value one as they can
    # achieve that reward and there is no other ways to get a reward since the
    # previous reward must have been accounted for

    final_adjacent = find_all_adjacent(
        agent, final_states
    )  # [12, 13, 19, 20, 24]
    testing.assert_almost_equal(
        table[final_adjacent], np.ones(len(final_adjacent)), difference_digits
    )

    # reward adjacent states after the first reward should be discounted
    # these are the states that are adjacent but after the first reward
    reward_adjacent = find_all_adjacent(
        agent, final_adjacent
    )  # [7, 8, 15, 18, 23]
    testing.assert_almost_equal(
        table[reward_adjacent],
        np.full(len(reward_adjacent), discount_rate),
        difference_digits,
    )

    # discount should compound
    reward_adjacent_adjacent = find_all_adjacent(agent, reward_adjacent)
    testing.assert_almost_equal(
        table[reward_adjacent_adjacent],
        np.full(len(reward_adjacent_adjacent), np.power(discount_rate, 3)),
        difference_digits,
    )

    # immediate reward and discounted reward should be considered
    discount_reward_adjacent = find_reward_and_discount_adjacent(agent)
    testing.assert_almost_equal(
        table[discount_reward_adjacent],
        np.power(discount_rate, 3) + 1,
        difference_digits,
    )


def test_policy_evaluation(dynamics: CollectionDynamics):
    discount_rate = 0.9
    agent = ValueIterationAgent(discount_rate, dynamics)

    # the minimum number of actions to achieve all the reward
    minimum_goal_steps = 5

    dd = DynamicsDistribution(100, dynamics)
    dd.compile()
    final_states = find_final_states(dd)

    state = dynamics.initial_state_id()
    for _itteration in range(minimum_goal_steps):
        assert state not in final_states
        action = agent.evaluate_policy(state)
        next_state, reward = dynamics.next_state_id(state, action)
        agent.record_transition(state, action, next_state, reward)
        state = next_state
    assert state in final_states
