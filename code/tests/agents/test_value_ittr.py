from .agent_dynamics_mock import VacuumDynamics, TestAgentConfig, VacuumStates
from src.model.dynamics.actions import Action
from src.model.agents.value_iteration.agent import ValueIterationAgent
from src.model.agents.value_iteration.dynamics_distribution import (
    DynamicsDistribution,
)
from numpy import testing
import numpy as np


def test_get_table():
    test_config = TestAgentConfig()
    discount_rate = test_config.discount_rate()
    test_dynamics = VacuumDynamics()
    agent = ValueIterationAgent(test_config, test_dynamics)
    difference_digits = test_config.stopping_epsilon()
    table = agent.get_value_table()

    # final states should have no value as they are accumulate and provide no
    # more reward
    testing.assert_almost_equal(
        table[VacuumStates.cc.value], 0, difference_digits
    )

    # values adjacent to the final state should have value one as they can
    # achieve that reward and there is no other ways to get a reward since the
    # previous reward must have been accounted for

    final_adjacent = [VacuumStates.dcl.value, VacuumStates.cdr.value]
    testing.assert_almost_equal(
        table[final_adjacent], np.ones(len(final_adjacent)), difference_digits
    )

    # reward adjacent states after the first reward should be discounted
    # these are the states that are adjacent but after the first reward
    reward_adjacent = [VacuumStates.dcr.value, VacuumStates.cdl.value]
    testing.assert_almost_equal(
        table[reward_adjacent],
        np.full(len(reward_adjacent), discount_rate),
        difference_digits,
    )

    # immediate reward and discounted reward should be considered
    discount_reward_adjacent = [VacuumStates.ddl.value, VacuumStates.ddr.value]
    testing.assert_almost_equal(
        table[discount_reward_adjacent],
        np.full(len(discount_reward_adjacent), np.power(discount_rate, 2) + 1),
        difference_digits,
    )


def test_policy_evaluation():
    test_config = TestAgentConfig()
    test_dynamics = VacuumDynamics()
    agent = ValueIterationAgent(test_config, test_dynamics)

    optimal_actions = {
        VacuumStates.ddl.value: Action.up,
        VacuumStates.ddr.value: Action.up,
        VacuumStates.cdl.value: Action.right,
        VacuumStates.cdr.value: Action.up,
        VacuumStates.dcl.value: Action.up,
        VacuumStates.dcr.value: Action.left,
    }

    for state, optimal_action in optimal_actions.items():
        action = agent.evaluate_policy(state)
        assert action == optimal_action
