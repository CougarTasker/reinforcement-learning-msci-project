from typing import Optional

from ..model.agents.base_agent import BaseAgent
from ..model.agents.value_iteration.agent import ValueIterationAgent
from ..model.config.reader import ConfigReader
from ..model.dynamics.base_dynamics import BaseDynamics
from ..model.dynamics.collection_dynamics import CollectionDynamics
from .options import AgentOptions, DynamicsOptions


class AgentEnvironmentFactory(object):
    """Factory method for abstracting agent and dynamics construction."""

    def __init__(
        self,
        agent: AgentOptions,
        dynamics: DynamicsOptions,
    ) -> None:
        """Create the factory.

        each factory instance can only build instance to keep consistency, as
        each dynamics will have its own state numbering system and each agent
        will depend on that.

        Args:
            agent (AgentOptions): which agent to create
            dynamics (DynamicsOptions): which dynamics to create
        """
        config_reader = ConfigReader()
        self.agent_config = config_reader.agent()
        self.dynamics_config = config_reader.grid_world()
        self.agent_option = agent
        self.dynamics_option = dynamics
        self.agent: Optional[BaseAgent] = None
        self.dynamics: Optional[BaseDynamics] = None

    def get_dynamics(self) -> BaseDynamics:
        """Get the dynamics.

        Raises:
            ValueError: if the dynamics option specified is unknown.

        Returns:
            BaseDynamics: the dynamics instance, the returned class will be a
            concrete instance that extends `BaseDynamics`
        """
        if self.dynamics is not None:
            # reuse existing dynamics to avoid inconsistencies
            return self.dynamics

        match self.dynamics_option:
            case DynamicsOptions.collection:
                self.dynamics = CollectionDynamics(self.dynamics_config)
            case _:
                raise ValueError(
                    f"unknown dynamics {self.dynamics_option.name}"
                )

        return self.dynamics

    def get_agent(self) -> BaseAgent:
        """Get the agent.

        this will perform any necessary setup, this may take time consider
        offloading this to another thread

        Raises:
            ValueError: if the agent specified is not known

        Returns:
            BaseAgent: the agent to instance. this agent is to be used with the
            dynamics provided to avoid inconsistencies.
        """
        if self.agent is not None:
            return self.agent

        match self.agent_option:
            case AgentOptions.value_iteration:
                self.agent = ValueIterationAgent(
                    self.agent_config, self.get_dynamics()
                )

                # take the value table hit now rather than on the first
                # iteration allows us to add a loading bar for it etc keep the
                # application more interactive
                self.agent.get_value_table()
            case _:
                raise ValueError(f"unknown agent {self.agent_option.name}")

        return self.agent
