from enum import IntEnum


# it is important the actions be zero based it is an assumption used by the
# q-learning agent.
class Action(IntEnum):
    """Enumerates all possible actions."""

    up = 0
    down = 1
    left = 2
    right = 3
