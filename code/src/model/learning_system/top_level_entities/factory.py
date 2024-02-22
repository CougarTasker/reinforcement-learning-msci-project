from src.model.agents.base_agent import BaseAgent
from src.model.agents.q_learning.agent import QLearningAgent
from src.model.agents.value_iteration.agent import ValueIterationAgent
from src.model.agents.value_iteration.agent_optimised import (
    ValueIterationAgentOptimised,
)
from src.model.config.reader import ConfigReader
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.dynamics.cliff_dynamics import CliffDynamics
from src.model.dynamics.collection_dynamics import CollectionDynamics
from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
)
from src.model.learning_system.learning_instance.statistics_recorder import (
    StatisticsRecorder,
)
from src.model.learning_system.top_level_entities.container import (
    EntityContainer,
)

from .options import AgentOptions, DynamicsOptions, TopEntitiesOptions


class EntityFactory(object):
    """Factory class for creating entities from the given options."""

    @classmethod
    def create_entities(
        cls,
        options: TopEntitiesOptions,
        hyper_parameters: BaseHyperParameterStrategy,
    ) -> EntityContainer:
        """Create new entities from the given options.

        Args:
            options (TopEntitiesOptions): the options that describe which
                entities to create.
            hyper_parameters (BaseHyperParameterStrategy): the parameters for
                these entities.

        Returns:
            EntityContainer: The new entities.
        """
        dynamics = cls.create_dynamics(options)
        agent = cls.create_agent(options, hyper_parameters, dynamics)
        stats = StatisticsRecorder()
        return EntityContainer(agent, dynamics, stats, options)

    @classmethod
    def create_agent(
        cls,
        options: TopEntitiesOptions,
        hyper_parameters: BaseHyperParameterStrategy,
        dynamics: BaseDynamics,
    ) -> BaseAgent:
        """Create the agent based upon these options.

        Args:
            options (TopEntitiesOptions): the options that describe what agent
                to create.
            hyper_parameters (BaseHyperParameterStrategy): the hyper parameters
                the agent should use.
            dynamics (BaseDynamics): the dynamics that are used by the value
                iteration agent.

        Raises:
            ValueError: if the agent specified is not known

        Returns:
            BaseAgent: the agent to instance. this agent is to be used with the
            dynamics provided to avoid inconsistencies.
        """
        match options.agent:
            case AgentOptions.value_iteration:
                return ValueIterationAgent(hyper_parameters, dynamics)
            case AgentOptions.value_iteration_optimised:
                return ValueIterationAgentOptimised(hyper_parameters, dynamics)
            case AgentOptions.q_learning:
                return QLearningAgent(
                    hyper_parameters,
                    options.exploration_strategy,
                    dynamics.state_count_upper_bound(),
                )
            case _:
                raise ValueError(f"unknown agent {options.agent.name}")

    @classmethod
    def create_dynamics(cls, options: TopEntitiesOptions) -> BaseDynamics:
        """Create the dynamics appropriate for these options.

        Args:
            options (TopEntitiesOptions): the options that describe what
                dynamics to create.

        Raises:
            ValueError: if the dynamics option specified is unknown.

        Returns:
            BaseDynamics: the dynamics instance, the returned class will be a
            concrete instance that extends `BaseDynamics`
        """
        dynamic_config = ConfigReader().grid_world
        match options.dynamics:
            case DynamicsOptions.collection:
                return CollectionDynamics(dynamic_config)
            case DynamicsOptions.cliff:
                return CliffDynamics(dynamic_config)
            case _:
                raise ValueError(f"unknown dynamics {options.dynamics.name}")
