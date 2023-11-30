from src.model.agents.value_iteration.dynamics_distribution import (
    DynamicsDistribution,
)
from tests.agents.agent_dynamics_mock import VacuumDynamics


def test_get_numpy_arrays():
    dd = DynamicsDistribution(100, VacuumDynamics())

    dd.observations = {
        0: {
            1: {0: (0, 0.5), 1: (1, 0.5)},
            2: {2: (2, 0.3), 3: (3, 0.3), 4: (4, 0.3)},
        },
        1: {1: {5: (5, 1)}, 2: {6: (6, 1)}},
        2: {1: {7: (7, 0.5), 8: (8, 0.5)}, 2: {9: (9, 0.5), 10: (10, 0.5)}},
    }

    (
        lookup_table,
        next_state,
        expected_reward,
        frequency,
    ) = dd.get_array_representation()

    assert lookup_table[0, 0, 0] == 0
    assert lookup_table[0, 0, 1] == 2
    assert lookup_table[0, 1, 0] == 2
    assert lookup_table[0, 1, 1] == 5

    assert next_state[lookup_table[1, 0, 0]] == 5
    assert lookup_table[1, 0, 0] + 1 == lookup_table[1, 0, 1]
    assert next_state[lookup_table[1, 0, 0]] == 5
    assert next_state[lookup_table[1, 1, 0]] == 6

    assert expected_reward[lookup_table[1, 0, 0]] == 5
    assert expected_reward[lookup_table[1, 1, 0]] == 6

    assert frequency[lookup_table[1, 0, 0]] == 1
    assert frequency[lookup_table[1, 1, 0]] == 1
