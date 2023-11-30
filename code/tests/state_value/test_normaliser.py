from src.model.dynamics.actions import Action
from src.model.learning_system.value_range_normaliser.normaliser_factory import (
    NormaliserFactory,
)
from tests.state_value.mocks import SimpleTestDynamics, MockAgent


def test_normaliser_factory():
    factory = NormaliserFactory(
        MockAgent(-10, 100, -55, 12), SimpleTestDynamics(), True
    )

    normaliser_l = factory.create_normaliser(0)
    normaliser_le = factory.create_normaliser(1)
    normaliser_re = factory.create_normaliser(2)
    normaliser_r = factory.create_normaliser(3)

    assert normaliser_l is normaliser_r
    assert normaliser_le is normaliser_re
    assert normaliser_l is not normaliser_le


def test_normaliser_function():
    state_min = -19
    state_max = 100
    action_min = 0
    action_max = 100
    factory = NormaliserFactory(
        MockAgent(state_min, state_max, action_min, action_max),
        SimpleTestDynamics(),
        False,
    )

    normaliser_non_ent = factory.create_normaliser(0)
    normaliser_ent = factory.create_normaliser(1)

    assert normaliser_non_ent.get_state_value_normalised((0, 0)) == 0
    assert normaliser_non_ent.get_state_value_normalised((1, 0)) == 0.5
    assert normaliser_ent.get_state_value_normalised((0, 0)) == 1
    assert normaliser_ent.get_state_value_normalised((1, 0)) == 1

    assert (
        normaliser_ent.get_state_action_value_normalised((0, 0), Action.up) == 0
    )
    assert (
        normaliser_ent.get_state_action_value_normalised((0, 0), Action.down)
        == 0
    )
    assert (
        normaliser_ent.get_state_action_value_normalised((0, 0), Action.left)
        == 1
    )
    assert (
        normaliser_ent.get_state_action_value_normalised((0, 0), Action.right)
        == 0.5
    )


def test_normaliser_cache():
    agent = MockAgent(0, 100, -55, 12)
    factory = NormaliserFactory(agent, SimpleTestDynamics(), True)

    normaliser_one = factory.create_normaliser(0)

    assert normaliser_one.get_state_value_normalised((0, 0)) == 0

    agent.state_values[0] = 75
    # check the normaliser uses cached values although out of date

    normaliser_two = factory.create_normaliser(3)

    assert normaliser_two.get_state_value_normalised((0, 0)) == 0


def test_no_cache():
    agent = MockAgent(0, 100, -55, 12)
    factory = NormaliserFactory(agent, SimpleTestDynamics(), False)

    normaliser_one = factory.create_normaliser(0)

    assert normaliser_one.get_state_value_normalised((0, 0)) == 0

    agent.state_values[0] = 75
    # check the normaliser does not use the out of data values

    normaliser_two = factory.create_normaliser(3)

    assert normaliser_two.get_state_value_normalised((0, 0)) == 0.5
