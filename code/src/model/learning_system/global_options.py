from dataclasses import dataclass

from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.agent import QLearningAgent
from src.model.agents.value_iteration.agent import ValueIterationAgent
from src.model.agents.value_iteration.agent_optimised import (
    ValueIterationAgentOptimised,
)
from src.model.config.reader import ConfigReader
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.dynamics.cliff_dynamics import CliffDynamics
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.options import (
    AgentOptions,
    AutomaticOptions,
    DynamicsOptions,
)

from ..agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from ..dynamics.collection_dynamics import CollectionDynamics


@dataclass(frozen=True, slots=True)
class TopEntitiesOptions(object):
    """Class that represents the options for the top level entities."""

    agent: AgentOptions
    dynamics: DynamicsOptions
    exploration_strategy: ExplorationStrategyOptions

    def create_agent(self, dynamics: BaseDynamics) -> BaseAgent:
        """Create the agent based upon these options.

        Args:
            dynamics (BaseDynamics): the dynamics that are used by the value
                iteration agent.

        Raises:
            ValueError: if the agent specified is not known

        Returns:
            BaseAgent: the agent to instance. this agent is to be used with the
            dynamics provided to avoid inconsistencies.
        """
        agent_config = ConfigReader().agent()
        match self.agent:
            case AgentOptions.value_iteration:
                return ValueIterationAgent(agent_config, dynamics)
            case AgentOptions.value_iteration_optimised:
                return ValueIterationAgentOptimised(agent_config, dynamics)
            case AgentOptions.q_learning:
                return QLearningAgent(
                    agent_config,
                    self.exploration_strategy,
                )
            case _:
                raise ValueError(f"unknown agent {self.agent.name}")

    def create_dynamics(self) -> BaseDynamics:
        """Create the dynamics appropriate for these options.

        Raises:
            ValueError: if the dynamics option specified is unknown.

        Returns:
            BaseDynamics: the dynamics instance, the returned class will be a
            concrete instance that extends `BaseDynamics`
        """
        dynamic_config = ConfigReader().grid_world()
        match self.dynamics:
            case DynamicsOptions.collection:
                return CollectionDynamics(dynamic_config)
            case DynamicsOptions.cliff:
                return CliffDynamics(dynamic_config)
            case _:
                raise ValueError(f"unknown dynamics {self.dynamics.name}")


@dataclass(frozen=True, slots=True)
class GlobalOptions(object):
    """Class represents the current options."""

    top_level_options: TopEntitiesOptions
    display_mode: DisplayMode
    automatic: AutomaticOptions
