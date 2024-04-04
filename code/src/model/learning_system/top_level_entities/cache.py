from typing import Dict

from src.model.hyperparameters.config_parameter_strategy import (
    ParameterConfigStrategy,
)
from src.model.learning_system.global_options import TopEntitiesOptions
from src.model.learning_system.top_level_entities.container import (
    EntityContainer,
)
from src.model.learning_system.top_level_entities.factory import EntityFactory


class TopEntitiesCache(object):
    """Cache for top level entities keeping consistency."""

    cache: Dict[TopEntitiesOptions, EntityContainer] = {}

    def get_entities(self, options: TopEntitiesOptions) -> EntityContainer:
        """Get top level entities from specified options.

        If a cached option exists this will be returned.

        Args:
            options (TopEntitiesOptions): the options that specify how the top
                level entities should be.

        Returns:
            EntityContainer: The entities based upon the options.
        """
        entities = self.cache.get(options, None)

        if entities is not None:
            return entities
        return self.create_new_entities(options)

    def create_new_entities(
        self, options: TopEntitiesOptions
    ) -> EntityContainer:
        """Get top level entities from specified options.

        This circumvents the cache and updates its value.

        Args:
            options (TopEntitiesOptions): the options that specify how the top
                level entities should be.

        Returns:
            EntityContainer: The entities based upon the options.
        """
        hyper_parameters = ParameterConfigStrategy()
        entities = EntityFactory.create_entities(options, hyper_parameters)
        self.cache[options] = entities
        return entities
