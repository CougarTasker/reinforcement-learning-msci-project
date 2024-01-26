from src.model.dynamics.actions import Action
from src.model.learning_system.value_standardisation.normaliser_factory import (
    NormaliserFactory,
)
from tests.state_value.mocks import MockAgent, SimpleTestDynamics


def test_mock_dynamics():
    d = SimpleTestDynamics()
    assert d.left.agent_location == (0, 0)
    assert d.right.agent_location == (1, 0)
    assert d.left_entity.agent_location == (0, 0)
    assert d.right_entity.agent_location == (1, 0)

    assert d.left.entities.get((0, 0)) is None
    assert d.right.entities.get((0, 0)) is None
    assert d.left_entity.entities.get((0, 0)) is not None
    assert d.right_entity.entities.get((0, 0)) is not None

    assert d.left.entities == d.right.entities
    assert d.left_entity.entities == d.right_entity.entities
    assert d.left.entities != d.left_entity.entities

    assert d.state_pool.get_state_id(d.left) == 0
    assert d.state_pool.get_state_id(d.right) == 1
    assert d.state_pool.get_state_id(d.left_entity) == 2
    assert d.state_pool.get_state_id(d.right_entity) == 3


def test_normaliser_factory():
    factory = NormaliserFactory(
        MockAgent(-10, 100, -55, 12), SimpleTestDynamics(), True
    )

    normaliser_l = factory.create_normaliser(0)
    normaliser_r = factory.create_normaliser(1)
    normaliser_le = factory.create_normaliser(2)
    normaliser_re = factory.create_normaliser(3)

    assert normaliser_l is normaliser_r
    assert normaliser_le is normaliser_re
    assert normaliser_l is not normaliser_le


def test_normaliser_function():
    state_min = -19
    state_max = 100
    action_min = 0
    action_max = 100
    dynamics = SimpleTestDynamics()
    factory = NormaliserFactory(
        MockAgent(state_min, state_max, action_min, action_max),
        dynamics,
        False,
    )

    normaliser_non_ent = factory.create_normaliser(0)
    normaliser_ent = factory.create_normaliser(2)

    assert normaliser_non_ent.get_state_value_normalised(dynamics.left) == 0
    assert normaliser_non_ent.get_state_value_normalised(dynamics.right) == 0.5
    assert normaliser_ent.get_state_value_normalised(dynamics.left_entity) == 1
    assert normaliser_ent.get_state_value_normalised(dynamics.right_entity) == 1

    assert (
        normaliser_ent.get_state_action_value_normalised(
            dynamics.left_entity, Action.up
        )
        == 0
    )
    assert (
        normaliser_ent.get_state_action_value_normalised(
            dynamics.left_entity, Action.down
        )
        == 0
    )
    assert (
        normaliser_ent.get_state_action_value_normalised(
            dynamics.left_entity, Action.left
        )
        == 1
    )
    assert (
        normaliser_ent.get_state_action_value_normalised(
            dynamics.left_entity, Action.right
        )
        == 0.5
    )


def test_normaliser_cache():
    agent = MockAgent(0, 100, -55, 12)
    dynamics = SimpleTestDynamics()
    factory = NormaliserFactory(agent, dynamics, True)

    normaliser_one = factory.create_normaliser(0)

    assert normaliser_one.get_state_value_normalised(dynamics.left) == 0

    agent.state_values[0] = 75
    # check the normaliser uses cached values although out of date

    normaliser_two = factory.create_normaliser(1)

    assert normaliser_two.get_state_value_normalised(dynamics.left) == 0


def test_no_cache():
    agent = MockAgent(0, 100, -55, 12)
    dynamics = SimpleTestDynamics()
    factory = NormaliserFactory(agent, dynamics, False)

    normaliser_one = factory.create_normaliser(0)

    assert normaliser_one.get_state_value_normalised(dynamics.left) == 0

    agent.state_values[0] = 75
    # check the normaliser does not use the out of data values

    normaliser_two = factory.create_normaliser(3)

    assert normaliser_two.get_state_value_normalised(dynamics.left) == 0.5
