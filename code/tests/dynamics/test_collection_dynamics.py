from itertools import cycle

import numpy as np
from pytest import fixture

from src.model.dynamics.actions import Action
from src.model.dynamics.collection_dynamics import CollectionDynamics
from src.model.dynamics.grid_world import GridWorld

from .mini_config import MockGridWorldConfig

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
    locations_mock.side_effect = cycle(
        [
            test_goal_a,
            test_goal_b,
        ]
    )
    return CollectionDynamics(MockGridWorldConfig())


def test_fixture(dynamics: CollectionDynamics):
    assert dynamics.grid_world.width == MockGridWorldConfig().width()
    assert dynamics.grid_world.height == MockGridWorldConfig().height()
    test_gw = GridWorld(1, 1)
    assert test_gw.random_in_bounds_cell() == test_goal_a
    assert test_gw.random_in_bounds_cell() == test_goal_b


def test_initial_state(dynamics: CollectionDynamics):
    start = dynamics.initial_state()

    assert start.agent_location == MockGridWorldConfig().agent_location()
    assert start.agent_energy == MockGridWorldConfig().initial_energy()
    assert len(start.entities) == MockGridWorldConfig().entity_count()


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


def expected_state_count():
    state_grid = 3 * 3
    # positions without collecting + collect a first + collect b first +
    # both collected accumulating states
    return state_grid - 2 + (state_grid - 1) * 2 + 2


def test_state_count(dynamics: CollectionDynamics):
    state = dynamics.initial_state_id()

    states_to_visit = [state]
    seen_states = set(states_to_visit)
    sections = []
    while states_to_visit:
        cur = states_to_visit.pop(0)
        for action in Action:
            next_state, r = dynamics.next_state_id(cur, action)
            sections.append((cur, next_state, action, r))
            if next_state not in seen_states:
                seen_states.add(next_state)
                states_to_visit.append(next_state)

    paths = []

    for cur, next_state, action, r in sections:
        paths.append(f'{cur} -> {next_state} [label="{action.name}, {r}"];')
    print("\n".join(paths))
    assert len(seen_states) == expected_state_count()


def test_consistent_initial_state(dynamics: CollectionDynamics):
    state_a = dynamics.initial_state()
    state_b = dynamics.initial_state()
    assert state_a == state_b

    id_a = dynamics.initial_state_id()
    id_b = dynamics.initial_state_id()

    assert id_a == id_b
