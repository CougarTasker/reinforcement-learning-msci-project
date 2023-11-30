from enum import Enum


class AgentOptions(Enum):
    """Enumerates the possible agents."""

    value_iteration = 1
    q_learning = 2


class DynamicsOptions(Enum):
    """Enumerates the possible agents."""

    collection = 1
