import numpy as np

from .actions import Action


class GridWorld(object):
    """Provide common functionality for working with a grid world."""

    def __init__(self, width: int, height: int) -> None:
        """Initialise a grid world with a given size.

        Raises:
            TypeError: If the width or height are not integers
            ValueError: if the width or height are not positive integer

        Args:
            width (int): The width of the grid world.
            height (int): The height of the gird world.
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be valid integers")
        elif width < 1 or height < 1:
            raise ValueError("width and height must be positive integers")

        self.width = width
        self.height = height

    def is_in_bounds(self, position: tuple[int, int]) -> bool:
        """Detect either a position is within the bounds of the grid.

        Args:
            position (tuple[int, int]): the position to test

        Returns:
            bool: true where the position is within the bounds of the grid
            world.
        """
        x_pos, y_pos = position
        return 0 <= x_pos < self.width and 0 <= y_pos < self.height

    def random_in_bounds_cell(self) -> tuple[int, int]:
        """Generate a random cell position that is within bounds.

        Returns:
            tuple[int, int]: the cell position within the grid.
        """
        dimensions = np.array([self.width, self.height])
        position = np.random.rand(2) * dimensions
        return tuple(np.floor(position).astype(int))

    def movement_action(
        self,
        current_position: tuple[int, int],
        action: Action,
        distance: int = 1,
    ) -> tuple[int, int]:
        """Calculate the adjacent cell in a given direction.

        The direction is provided from the up,down,left and right actions. This
        method calculates the next position assuming the origin is at the bottom
        left of the grid.

        note this may compute a cell that is out of bounds, to check and handel
        this please use `is_in_bounds` method.

        Args:
            current_position (tuple[int, int]): the position to start from.
            action (Action): provides the direction to move in.
            distance (int): the amount of cells to move. Defaults to 1.

        Raises:
            ValueError: If the action provided is not a known movement action.

        Returns:
            tuple[int, int]: The position after moving.
        """
        x_pos, y_pos = current_position
        match action:
            case Action.up:
                return (x_pos, y_pos + distance)
            case Action.down:
                return (x_pos, y_pos - distance)
            case Action.left:
                return (x_pos - distance, y_pos)
            case Action.right:
                return (x_pos + distance, y_pos)
            case _:
                raise ValueError(
                    f"Action {action.name} is not a known movement action"
                )
