from dataclasses import dataclass, replace

from typing_extensions import Self

from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.learning_system.global_options import GlobalOptions

from ..agents import BaseAgent


@dataclass(frozen=True)
class TopLevelEntities(object):
    """Class that encompasses the top level entities of the learning system."""

    agent: BaseAgent
    dynamics: BaseDynamics
    options: GlobalOptions

    @classmethod
    def create_new_entities(cls, options: GlobalOptions) -> Self:
        """Construct new top level entities from specified options.

        Args:
            options (GlobalOptions): the options that specify how the top level
                entities should be.

        Returns:
            Self: the new top level entities
        """
        dynamics = options.create_dynamics()
        agent = options.create_agent(dynamics)
        return cls(agent, dynamics, options)

    def update_options(self, options: GlobalOptions) -> "TopLevelEntities":
        """Construct new top level entities from specified options.

        unlike create new entities, this method will reuse where possible.

        Args:
            options (GlobalOptions): the options that specify how the top level
                entities should be.

        Returns:
            Self: the new top level entities.
        """
        if options == self.options:
            return self

        if self.options.dynamics is not options.dynamics:
            return self.create_new_entities(options)

        if self.options.agent is not options.agent:
            agent = options.create_agent(self.dynamics)
            return TopLevelEntities(agent, self.dynamics, options)

        return replace(self, options=options)
