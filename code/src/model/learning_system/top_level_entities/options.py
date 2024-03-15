from dataclasses import dataclass
from enum import Enum

from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)


class AgentOptions(Enum):
    """Enumerates the possible agents."""

    value_iteration_optimised = 1
    value_iteration = 2
    q_learning = 3


class DynamicsOptions(Enum):
    """Enumerates the possible agents."""

    collection = 1
    cliff = 2


@dataclass(frozen=True, slots=True)
class TopEntitiesOptions(object):
    """Class that represents the options for the top level entities."""

    agent: AgentOptions
    dynamics: DynamicsOptions
    exploration_strategy: ExplorationStrategyOptions
