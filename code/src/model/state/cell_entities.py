from enum import Enum


class CellEntity(Enum):
    """This class enumerates all the possible entities that may be in a cell."""

    agent = 1
    goal = 2
    empty = 3
    warning = 4
    wind_up = 5
    wind_left = 6
