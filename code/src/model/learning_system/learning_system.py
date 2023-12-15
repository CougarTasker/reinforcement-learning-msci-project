from typing import Optional

from ..agents import (
    BaseAgent,
    QLearningAgent,
    ValueIterationAgent,
    ValueIterationAgentOptimised,
)
from ..config.reader import ConfigReader
from ..dynamics.base_dynamics import BaseDynamics
from ..dynamics.collection_dynamics import CollectionDynamics
from .cell_configuration import DisplayMode
from .learning_instance import LearningInstance
from .options import AgentOptions, DynamicsOptions
from .state_description.state_description import StateDescription
from .state_description.state_description_factory import StateDescriptionFactory


class LearningSystem(object):
    """Controller for managing one pair of agent and dynamics."""

    def __init__(
        self,
        agent: AgentOptions,
        dynamics: DynamicsOptions,
    ) -> None:
        """Create the controller.

        each instance can only build instance to keep consistency, as
        each dynamics will have its own state numbering system and each agent
        will depend on that.

        Args:
            agent (AgentOptions): which agent to create
            dynamics (DynamicsOptions): which dynamics to create
        """
        self._agent_option = agent
        self._dynamics_option = dynamics
        self._agent: Optional[BaseAgent] = None
        self._dynamics: Optional[BaseDynamics] = None

        self._main_learning_instance: Optional[LearningInstance] = None
        self._state_description_factory: Optional[
            StateDescriptionFactory
        ] = None
        self._display_mode = DisplayMode.default

        self._agent_config = ConfigReader().agent()

    def get_dynamics(self) -> BaseDynamics:
        """Get the dynamics.

        Raises:
            ValueError: if the dynamics option specified is unknown.

        Returns:
            BaseDynamics: the dynamics instance, the returned class will be a
            concrete instance that extends `BaseDynamics`
        """
        if self._dynamics is not None:
            # reuse existing dynamics to avoid inconsistencies
            return self._dynamics

        dynamics_config = ConfigReader().grid_world()

        match self._dynamics_option:
            case DynamicsOptions.collection:
                self._dynamics = CollectionDynamics(dynamics_config)
            case _:
                raise ValueError(
                    f"unknown dynamics {self._dynamics_option.name}"
                )

        return self._dynamics

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
        if self._agent is not None:
            return self._agent

        match self._agent_option:
            case AgentOptions.value_iteration:
                self._agent = ValueIterationAgent(
                    self._agent_config, self.get_dynamics()
                )
            case AgentOptions.value_iteration_optimised:
                self._agent = ValueIterationAgentOptimised(
                    self._agent_config, self.get_dynamics()
                )
            case AgentOptions.q_learning:
                self._agent = QLearningAgent(self._agent_config)
            case _:
                raise ValueError(f"unknown agent {self._agent_option.name}")

        return self._agent

    def get_current_state(self) -> StateDescription:
        """Get the current state of the learning instance.

        Returns:
            StateDescription: the current configuration for this state.
        """
        instance = self.__get_learning_instance()
        return self.__state_id_to_description(instance.get_current_state())

    def perform_action(
        self,
    ):
        """Perform one action chosen by the agent."""
        self.__get_learning_instance().perform_action()

    def reset_state(self):
        """Reset the current state to the initial state."""
        instance = self.__get_learning_instance()
        instance.reset_state()

    def set_display_mode(self, display_mode: DisplayMode):
        """Set the learning instance's display mode.

        Args:
            display_mode (DisplayMode): how to display the learning instance
        """
        self._display_mode = display_mode

    def __state_id_to_description(self, state_id: int) -> StateDescription:
        if self._state_description_factory is None:
            self._state_description_factory = StateDescriptionFactory(
                self.get_agent(), self.get_dynamics(), self._display_mode
            )
        self._state_description_factory.display_mode = self._display_mode
        return self._state_description_factory.create_state_description(
            state_id
        )

    def __get_learning_instance(self):
        if self._main_learning_instance is not None:
            return self._main_learning_instance
        self._main_learning_instance = LearningInstance(
            self.get_agent(), self.get_dynamics()
        )
        return self._main_learning_instance
