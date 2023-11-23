from src.model.dynamics.actions import Action
from src.model.state_value.normaliser_factory import NormaliserFactory
from tests.state_value.mocks import SimpleTestDynamics, TestAgent


def test_normaliser_factory():
    factory = NormaliserFactory(
        TestAgent(-10, 100, -55, 12), SimpleTestDynamics()
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
        TestAgent(state_min, state_max, action_min, action_max),
        SimpleTestDynamics(),
    )

    normaliser_non_ent = factory.create_normaliser(0)
    normaliser_ent = factory.create_normaliser(1)

    assert normaliser_non_ent.get_state_value((0, 0)) == 0
    assert normaliser_non_ent.get_state_value((1, 0)) == 0.5
    assert normaliser_ent.get_state_value((0, 0)) == 1
    assert normaliser_ent.get_state_value((1, 0)) == 1

    assert normaliser_ent.get_state_action_value((0, 0), Action.up) == 0
    assert normaliser_ent.get_state_action_value((0, 0), Action.down) == 0
    assert normaliser_ent.get_state_action_value((0, 0), Action.left) == 1
    assert normaliser_ent.get_state_action_value((0, 0), Action.right) == 0.5


def test_normaliser_cache():
    agent = TestAgent(0, 100, -55, 12)
    factory = NormaliserFactory(agent, SimpleTestDynamics())

    normaliser_one = factory.create_normaliser(0)

    assert normaliser_one.get_state_value((0, 0)) == 0

    agent.state_values[0] = 50
    # check the normaliser uses cached values although out of date

    normaliser_two = factory.create_normaliser(3)

    assert normaliser_two.get_state_value((0, 0)) == 0
