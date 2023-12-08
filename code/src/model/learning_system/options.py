from enum import Enum


class AgentOptions(Enum):
    """Enumerates the possible agents."""

    value_iteration_optimised = 1
    value_iteration = 2
    q_learning = 3


class DynamicsOptions(Enum):
    """Enumerates the possible agents."""

    collection = 1
