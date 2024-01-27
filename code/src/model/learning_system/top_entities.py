from dataclasses import dataclass
from typing import Dict

from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.learning_system.global_options import TopEntitiesOptions

from ..agents import BaseAgent


@dataclass(frozen=True)
class TopLevelEntities(object):
    """Class that encompasses the top level entities of the learning system."""

    agent: BaseAgent
    dynamics: BaseDynamics
    options: TopEntitiesOptions


class TopEntitiesCache(object):
    """Cache for top level entities keeping consistency."""

    cache: Dict[TopEntitiesOptions, TopLevelEntities] = {}

    def get_entities(self, options: TopEntitiesOptions) -> TopLevelEntities:
        """Get top level entities from specified options.

        If a cached option exists this will be returned.

        Args:
            options (TopEntitiesOptions): the options that specify how the top
                level entities should be.

        Returns:
            TopLevelEntities: The entities based upon the options.
        """
        entities = self.cache.get(options, None)

        if entities is not None:
            return entities
        return self.create_new_entities(options)

    def create_new_entities(
        self, options: TopEntitiesOptions
    ) -> TopLevelEntities:
        """Get top level entities from specified options.

        This circumvents the cache and updates its value.

        Args:
            options (TopEntitiesOptions): the options that specify how the top
                level entities should be.

        Returns:
            TopLevelEntities: The entities based upon the options.
        """
        dynamics = options.create_dynamics()
        agent = options.create_agent(dynamics)
        entities = TopLevelEntities(agent, dynamics, options)
        self.cache[options] = entities
        return entities
