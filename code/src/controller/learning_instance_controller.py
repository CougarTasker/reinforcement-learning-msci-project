from typing import Optional

from ..model.agents.base_agent import BaseAgent
from ..model.agents.value_iteration.agent import ValueIterationAgent
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
        self.agent_option = agent
        self.dynamics_option = dynamics
        self.agent: Optional[BaseAgent] = None
        self.dynamics: Optional[BaseDynamics] = None
        self.current_state: Optional[int] = None

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

        dynamics_config = ConfigReader().grid_world()

        match self.dynamics_option:
            case DynamicsOptions.collection:
                self.dynamics = CollectionDynamics(dynamics_config)
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

        agent_config = ConfigReader().agent()

        match self.agent_option:
            case AgentOptions.value_iteration:
                self.agent = ValueIterationAgent(
                    agent_config, self.get_dynamics()
                )

                # take the value table hit now rather than on the first
                # iteration allows us to add a loading bar for it etc keep the
                # application more interactive
                self.agent.get_value_table()
            case _:
                raise ValueError(f"unknown agent {self.agent_option.name}")

        return self.agent

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
        self.current_state = next_state
        return (
            self.__state_id_to_description(last_state),
            action,
            self.__state_id_to_description(next_state),
            reward,
        )

    def __get_current_state_id(self) -> int:
        if self.current_state is not None:
            return self.current_state
        self.current_state = self.get_dynamics().initial_state_id()
        return self.current_state

    def __state_id_to_description(self, state_id: int) -> StateDescription:
        return StateDescription(self.get_dynamics(), state_id)
