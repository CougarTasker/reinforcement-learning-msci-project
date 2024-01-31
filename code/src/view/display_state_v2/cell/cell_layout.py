from typing import Tuple


class CellLayout(object):
    """Class for managing the layout and configuration of each cell."""

    min_border_width: int = 8
    min_padding: int = 2
    padding_ratio: float = 0.1
    border_ratio: float = 0.1

    def __init__(self, bounding_box: Tuple[int, int, int, int]):
        """Initialise the cell layout.

        Args:
            bounding_box (Tuple[int, int, int, int]): the size of the cell.
        """
        self.bounding_box = bounding_box
        self.cell_size = self.get_bounding_box_size(bounding_box)
        self.border_width = int(
            max(self.border_ratio * self.cell_size, self.min_border_width)
        )
        self.padding = int(
            max(self.padding_ratio * self.cell_size, self.min_padding)
        )

    def get_bounding_box_size(
        self, bounding_box: Tuple[int, int, int, int]
    ) -> int:
        """Get the size of a bounding box.

        Args:
            bounding_box (Tuple[int, int, int, int]): the box to measure

        Returns:
            int: the minimum length along one edge.
        """
        min_x, min_y, max_x, max_y = bounding_box

        return min(max_x - min_x, max_y - min_y)

    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Determine weather this cell contains a point.

        Checks its bounding box.

        Args:
            pos (Tuple[int, int]): the position to check

        Returns:
            bool: True if this point is in the bounding box
        """
        pos_x, pos_y = pos
        min_x, min_y, max_x, max_y = self.bounding_box
        return min_x <= pos_x <= max_x and min_y <= pos_y <= max_y

    def inset_bounding_box(
        self, inset_amount: int
    ) -> Tuple[int, int, int, int]:
        """Get the bounding box that has been inset.

        Args:
            inset_amount (int): the amount to make the box smaller

        Returns:
            Tuple[int, int, int, int]: the new bounding box that has been inset
        """
        min_x, min_y, max_x, max_y = self.bounding_box
        return (
            min_x + inset_amount,
            min_y + inset_amount,
            max_x - inset_amount,
            max_y - inset_amount,
        )
