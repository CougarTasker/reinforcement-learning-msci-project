from typing import Dict, Generator, Optional, Tuple

import numpy as np
from numpy.random import Generator as RandomGenerator

from .actions import Action

integer_position = Tuple[int, int]

location_generator = Generator[
    Tuple[integer_position, Tuple[int, int, int, int]], None, None
]


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

    def random_in_bounds_cell(
        self, random_generator: Optional[RandomGenerator] = None
    ) -> tuple[int, int]:
        """Generate a random cell position that is within bounds.

        Args:
            random_generator (Optional[RandomGenerator]): an optional random
                generator to pick the positions from.

        Returns:
            tuple[int, int]: the cell position within the grid.
        """
        if random_generator is None:
            random_generator = np.random.default_rng()
        dimensions = np.array([self.width, self.height])
        position_float = random_generator.random(2) * dimensions
        position_integer = np.floor(position_float).astype(int)
        return (position_integer[0], position_integer[1])

    action_direction: Dict[Action, integer_position] = {
        Action.up: (0, -1),
        Action.down: (0, 1),
        Action.right: (1, 0),
        Action.left: (-1, 0),
    }

    def movement_action(
        self,
        current_position: integer_position,
        action: Action,
        distance: int = 1,
    ) -> integer_position:
        """Calculate the adjacent cell in a given direction.

        The direction is provided from the up,down,left and right actions. This
        method calculates the next position assuming the origin is at the top
        left of the grid.

        note this may compute a cell that is out of bounds, to check and handel
        this please use `is_in_bounds` method.

        Args:
            current_position (integer_position): the position to start from.
            action (Action): provides the direction to move in.
            distance (int): the amount of cells to move. Defaults to 1.

        Raises:
            ValueError: If the action provided is not a known movement action.

        Returns:
            integer_position: The position after moving.
        """
        x_pos, y_pos = current_position
        dir_x, dir_y = self.action_direction[action]
        return (x_pos + dir_x * distance, y_pos + dir_y * distance)

    def list_cells(self) -> Generator[integer_position, None, None]:
        """Generate all cells in the grid world.

        Yields:
            Generator[integer_position, None, None]: each cell location
        """
        for y_pos in range(self.height):
            yield from ((x_pos, y_pos) for x_pos in range(self.width))

    def get_cell_sizing(
        self, width: int, height: int, relative_margins: float
    ) -> Tuple[int, int]:
        """Get the sizing of a cell in the given rectangle and margins.

        Args:
            width (int): the width of the containing rectangle
            height (int): the hight of the containing rectangle
            relative_margins (float): how large should the gap between cells be.
                relative to the size of a cell with no margins

        Returns:
            Tuple[int, int]: the cell size and the margin size
        """
        rows = self.height
        columns = self.width

        content_ratio = rows / columns
        container_ratio = height / width
        side_margins = container_ratio < content_ratio

        cell_spacing = int(height / rows if side_margins else width / columns)
        margins = int(max(cell_spacing * relative_margins, 1))

        return cell_spacing, margins

    def get_grid_bounds(
        self, width: int, height: int, relative_margins: float
    ) -> Tuple[int, int, int, int]:
        """Get the bounding box of a grid.

        Args:
            width (int): the width of the containing rectangle
            height (int): the hight of the containing rectangle
            relative_margins (float): how large should the gap between cells be.
            relative to the size of a cell with no margins

        Returns:
            Tuple[int, int, int, int]: the bounding box of where the grid will
                be.
        """
        rows = self.height
        columns = self.width

        cell_spacing, margins = self.get_cell_sizing(
            width, height, relative_margins
        )

        offset_min_x = int((width - columns * cell_spacing) / 2)
        offset_min_y = int((height - rows * cell_spacing) / 2)

        offset_min_x += margins // 2
        offset_min_y += margins // 2

        offset_max_x = offset_min_x + cell_spacing - margins
        offset_max_y = offset_min_y + cell_spacing - margins
        return offset_min_x, offset_min_y, offset_max_x, offset_max_y

    def list_cell_positions(
        self, width: int, height: int, relative_margins: float
    ) -> location_generator:
        """Generate the cell locations in a given rectangle.

        the cells will be centred if there is the aspect ratio's are not aligned

        returns the cell position in gird world coordinates, the location of
        corner that is closest to the origin then the corner that is the
        furthest.

        assumes cells should be square.

        Args:
            width (int): the width of the containing rectangle
            height (int): the hight of the containing rectangle
            relative_margins (float): how large should the gap between cells be.
                relative to the size of a cell with no margins

        Yields:
            Iterator[location_generator]: the coordinates
        """
        cell_spacing = self.get_cell_sizing(width, height, relative_margins)[0]
        (
            offset_min_x,
            offset_min_y,
            offset_max_x,
            offset_max_y,
        ) = self.get_grid_bounds(width, height, relative_margins)
        for pos in self.list_cells():
            bounding_box = (
                offset_min_x + cell_spacing * pos[0],
                offset_min_y + cell_spacing * pos[1],
                offset_max_x + cell_spacing * pos[0],
                offset_max_y + cell_spacing * pos[1],
            )
            yield pos, bounding_box
