from enum import Enum


class CellEntity(Enum):
    """This class enumerates all the possible entities that may be in a cell."""

    agent = 1
    goal = 2
    empty = 3
    blocked = 4
