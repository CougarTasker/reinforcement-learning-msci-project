from .test_collection_dynamics import dynamics
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.agents.value_iteration.dynamics_distribution import (
    DynamicsDistribution,
)
from timeit import timeit
import numpy as np
from .test_collection_dynamics import expected_state_count


def test_sequential_integers(dynamics: BaseDynamics):
    dist = DynamicsDistribution(100, dynamics)
    dist.compile()

    states = np.array(list(dist.observations.keys()))
    states.sort()

    assert states[0] == 0
    assert np.all(np.diff(states) == 1)


def test_duration(dynamics: BaseDynamics):
    dist = DynamicsDistribution(100, dynamics)

    assert not dynamics.is_stochastic()
    # Should ignore sample count for deterministic dynamics
    assert dist.sample_count == 1

    assert timeit(dist.compile, number=100) < 1


def test_state_count(dynamics: BaseDynamics):
    dist = DynamicsDistribution(100, dynamics)

    dist.compile()
    
    assert dist.get_state_count() == expected_state_count()
