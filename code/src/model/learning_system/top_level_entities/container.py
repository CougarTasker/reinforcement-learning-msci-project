from dataclasses import dataclass

from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.learning_system.learning_instance.statistics_recorder import (
    StatisticsRecorder,
)
from src.model.learning_system.top_level_entities.options import (
    TopEntitiesOptions,
)


@dataclass(frozen=True, slots=True)
class EntityContainer(object):
    """Class that encompasses the top level entities of the learning system."""

    agent: BaseAgent
    dynamics: BaseDynamics
    statistics: StatisticsRecorder
    options: TopEntitiesOptions
