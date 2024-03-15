from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.dynamics.grid_world import GridWorld
from src.model.learning_system.learning_instance.statistics_recorder import (
    StatisticsRecorder,
)
from src.model.learning_system.top_level_entities.container import (
    EntityContainer,
)
from src.model.state.state_pool import StatePool


class BaseEntityDecorator(object):
    """Base class for Wrapper classes of the top level entities."""

    def __init__(self, entities: EntityContainer) -> None:
        """Initialise the decorator.

        Args:
            entities (EntityContainer): The entities the cell configuration is
                based upon.
        """
        self.entities = entities

    def update_entities(self, entities: EntityContainer) -> None:
        """Update the entities this wrapper uses internally.

        Args:
            entities (EntityContainer): The new entities used internally
        """
        self.entities = entities

    @property
    def grid_world(self) -> GridWorld:
        """Access the grid world.

        Returns:
            GridWorld: the grid world for these entities.
        """
        return self.entities.dynamics.grid_world

    @property
    def state_pool(self) -> StatePool:
        """Access the state pool.

        Returns:
            StatePool: the state pool uses by these entities.
        """
        return self.entities.dynamics.state_pool

    @property
    def agent(self) -> BaseAgent:
        """Access the agent of these entities.

        Returns:
            BaseAgent: the agent used by these entities
        """
        return self.entities.agent

    @property
    def dynamics(self) -> BaseDynamics:
        """Access the dynamics of these entities.

        Returns:
            BaseDynamics: the dynamics part of these entities
        """
        return self.entities.dynamics

    @property
    def statistics(self) -> StatisticsRecorder:
        """Access the statistics of these entities.

        Returns:
            StatisticsRecorder: the statistics part of these entities
        """
        return self.entities.statistics
