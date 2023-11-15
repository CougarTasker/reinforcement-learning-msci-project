from src.model.dynamics.grid_world import GridWorld
from src.model.dynamics.actions import Action
from pytest import raises
import numpy as np


def test_grid_world():
    test = GridWorld(3, 4)
    assert test.width == 3
    assert test.height == 4

    GridWorld(1, 1)

    with raises(Exception):
        GridWorld(0, 4)

    with raises(Exception):
        GridWorld(-1, -1)

    with raises(Exception):
        GridWorld("1", "1")


def test_in_bounds():
    test = GridWorld(3, 3)

    assert test.is_in_bounds((0, 0))
    assert test.is_in_bounds((1, 1))
    assert test.is_in_bounds((2, 1))
    assert test.is_in_bounds((0, 2))
    assert not test.is_in_bounds((-1, 0))
    assert not test.is_in_bounds((3, 0))
    assert not test.is_in_bounds((3, 3))


def test_random_gen(mocker):
    mock_random = mocker.patch("numpy.random.rand")

    test = GridWorld(3, 3)
    mock_random.return_value = np.array([0, 0])
    min_pos = test.random_in_bounds_cell()

    assert min_pos == (0, 0)
    almost_one = 1 - np.finfo(float).eps

    mock_random.return_value = np.array([almost_one, almost_one])
    max_pos = test.random_in_bounds_cell()

    assert max_pos == (2, 2)
    
def test_move():
    test = GridWorld(3, 3)

    assert test.movement_action((0, 0), Action.up) == (0, 1)
    assert test.movement_action((0, 0), Action.up, 5) == (0, 5)
    assert test.movement_action((2, 3), Action.up, 5) == (2, 8)

    assert test.movement_action((0, 0), Action.down) == (0, -1)
    assert test.movement_action((0, 0), Action.down, 4) == (0, -4)
    assert test.movement_action((2, 3), Action.down, 4) == (2, -1)

    assert test.movement_action((0, 0), Action.left) == (-1, 0)
    assert test.movement_action((0, 0), Action.left, 7) == (-7, 0)
    assert test.movement_action((6, 3), Action.left, 7) == (-1, 3)

    assert test.movement_action((0, 0), Action.right) == (1, 0)
    assert test.movement_action((0, 0), Action.right, 2) == (2, 0)
    assert test.movement_action((4, 5), Action.right, 2) == (6, 5)
