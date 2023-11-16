from .mini_config import TestConfig
from pytest import fixture
from src.model.dynamics.grid_world import GridWorld
from src.model.dynamics.collection_dynamics import CollectionDynamics
from src.model.dynamics.actions import Action

"""
Test Grid Initially:

 x G x
 x x A
 G x x

"""
test_goal_a = (1, 2)
test_goal_b = (0, 0)


@fixture
def dynamics(mocker):
    locations_mock = mocker.patch.object(GridWorld, "random_in_bounds_cell")
    locations_mock.side_effect = [
        test_goal_a,
        test_goal_b,
        (0, 0),
        (0, 0),
        (0, 0),
    ]
    return CollectionDynamics(TestConfig())


def test_fixture(dynamics: CollectionDynamics):
    assert dynamics.grid_world.width == TestConfig().width()
    assert dynamics.grid_world.height == TestConfig().height()
    test_gw = GridWorld(1, 1)
    assert test_gw.random_in_bounds_cell() == test_goal_a
    assert test_gw.random_in_bounds_cell() == test_goal_b


def test_initial_state(dynamics: CollectionDynamics):
    start = dynamics.initial_state()

    assert start.agent_location == TestConfig().agent_location()
    assert start.agent_energy == TestConfig().initial_energy()
    assert len(start.entities) == TestConfig().entity_count()


def test_dynamics(dynamics: CollectionDynamics):
    start = dynamics.initial_state()

    start_up = dynamics.next(start, Action.up)
    assert start_up[0].agent_location == (2, 2)
    assert start_up[1] == 0

    start_down = dynamics.next(start, Action.down)
    assert start_down[0].agent_location == (2, 0)
    assert start_down[1] == 0

    start_left = dynamics.next(start, Action.left)
    assert start_left[0].agent_location == (1, 1)
    assert start_left[1] == 0

    start_right = dynamics.next(start, Action.right)
    assert start_right[0] == start
    assert start_right[1] == 0

    # goal a

    goal_a_state = dynamics.next(start_left[0], Action.up)
    assert goal_a_state[0].agent_location == test_goal_a
    assert len(goal_a_state[0].entities) == 1
    assert goal_a_state[1] == 1

    # test loop

    top_right_with_goal = dynamics.next(goal_a_state[0], Action.right)[0]
    assert top_right_with_goal != start_up[0]
    assert top_right_with_goal.agent_location == start_up[0].agent_location

    # get to goal b
    start_left_with_goal = dynamics.next(goal_a_state[0], Action.down)

    assert start_left_with_goal[0] != start_left[0]
    assert (
        start_left_with_goal[0].agent_location == start_left[0].agent_location
    )
    assert start_left_with_goal[1] == 0

    goal_b_state = dynamics.next(
        dynamics.next(start_left_with_goal[0], Action.left)[0], Action.down
    )

    assert goal_b_state[0].agent_location == test_goal_b
    assert len(goal_b_state[0].entities) == 0
    assert goal_b_state[1] == 1

    # test absorbing

    absorbing_up = dynamics.next(goal_b_state[0], Action.up)
    assert absorbing_up[0] == goal_b_state[0]
    assert absorbing_up[1] == 0

    absorbing_right = dynamics.next(goal_b_state[0], Action.right)
    assert absorbing_right[0] == goal_b_state[0]
    assert absorbing_right[1] == 0
