from typing import Optional

from src.controller.cell_configuration import DisplayMode
from src.model.state_value.normaliser import StateValueNormaliser
from src.model.state_value.normaliser_factory import NormaliserFactory

from ..model.agents import BaseAgent, QLearningAgent, ValueIterationAgent
from ..model.config.reader import ConfigReader
from ..model.dynamics.actions import Action
from ..model.dynamics.base_dynamics import BaseDynamics
from ..model.dynamics.collection_dynamics import CollectionDynamics
from .options import AgentOptions, DynamicsOptions
from .state_description import StateDescription


class InstanceController(object):
    """Controller for managing one instance of a learning agent."""

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
        self._current_state: Optional[int] = None
        self._value_normalisation_factory: Optional[NormaliserFactory] = None
        self._display_mode = DisplayMode.default

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

        agent_config = ConfigReader().agent()

        match self._agent_option:
            case AgentOptions.value_iteration:
                self._agent = ValueIterationAgent(
                    agent_config, self.get_dynamics()
                )

                # take the value table hit now rather than on the first
                # iteration allows us to add a loading bar for it etc keep the
                # application more interactive
                self._agent.get_value_table()
            case AgentOptions.q_learning:
                self._agent = QLearningAgent(agent_config)
            case _:
                raise ValueError(f"unknown agent {self._agent_option.name}")

        return self._agent

    def get_current_state(self) -> StateDescription:
        """Get the current state of the learning instance.

        Returns:
            StateDescription: the current state instance
        """
        return self.__state_id_to_description(self.__get_current_state_id())

    def perform_action(
        self,
    ) -> tuple[StateDescription, Action, StateDescription, float]:
        """Perform one action chosen by the agent.

        Returns:
            tuple[StateDescription, Action, StateDescription, float]: the
            transition information, the last state, the action chosen, the next
            state, the reward received for this action.
        """
        last_state = self.__get_current_state_id()
        agent = self.get_agent()
        dynamics = self.get_dynamics()

        action = agent.evaluate_policy(last_state)
        next_state, reward = dynamics.next_state_id(last_state, action)
        agent.record_transition(last_state, action, next_state, reward)
        self._current_state = next_state
        return (
            self.__state_id_to_description(last_state),
            action,
            self.__state_id_to_description(next_state),
            reward,
        )

    def reset_state(self) -> StateDescription:
        """Reset the current state to the initial state.

        Returns:
            StateDescription: the initial state description and new current
            state.
        """
        self._current_state = self.get_dynamics().initial_state_id()
        return self.__state_id_to_description(self._current_state)

    def set_display_mode(self, display_mode: DisplayMode):
        """Set the learning instance's display mode.

        Args:
            display_mode (DisplayMode): how to display the learning instance
        """
        self._display_mode = display_mode

    def get_normaliser(self, state_id: int) -> StateValueNormaliser:
        """Get the normaliser for a given state.

        Args:
            state_id (int): the state to base the normaliser on

        Returns:
            StateValueNormaliser: the normaliser for this state
        """
        if self._value_normalisation_factory is None:
            self._value_normalisation_factory = NormaliserFactory(
                self.get_agent(), self.get_dynamics()
            )
        return self._value_normalisation_factory.create_normaliser(state_id)

    def __get_current_state_id(self) -> int:
        if self._current_state is not None:
            return self._current_state
        self._current_state = self.get_dynamics().initial_state_id()
        return self._current_state

    def __state_id_to_description(self, state_id: int) -> StateDescription:
        return StateDescription(
            self.get_dynamics(),
            state_id,
            self.get_normaliser(state_id),
            self._display_mode,
        )
