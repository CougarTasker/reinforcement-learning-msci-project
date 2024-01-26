from ..config.agent_section import AgentConfig
from ..dynamics.actions import Action


class BaseAgent(object):
    """Provides the common base for different learning agents."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialise an agent.

        Args:
            config (AgentConfig): the configuration for the agent.
        """
        self.config = config

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        Args:
            state (int): the state the agent is performing this action

        Raises:
            NotImplementedError: If this method has not been overridden by
                concrete agent.

        Returns:
            Action: the action to take in this state
        """
        self.__throw_not_implemented()
        return Action.down

    def record_transition(
        self,
        previous_state: int,
        previous_action: Action,
        new_state: int,
        reward: float,
    ) -> None:
        """Provide the agent with the information from a transition.

        Args:
            previous_state (int): the state before the action was taken
            previous_action (Action): the action that was taken.
            new_state (int): The resulting state after the action has been taken
            reward (float): the reward for performing this action

        Raises:
            NotImplementedError: If this method has not been overridden by
                concrete agent.
        """
        self.__throw_not_implemented()

    def get_state_value(self, state: int) -> float:
        """Get the agents interpretation of the value of this state.

        Args:
            state (int): the state to evaluate

        Raises:
            NotImplementedError: If this method has not been overridden by
                concrete agent.

        Returns:
            float: the agents interpretation of the value of this state
        """
        self.__throw_not_implemented()
        return 0

    def get_state_action_value(self, state: int, action: Action) -> float:
        """Get the agents interpretation of an actions value.

        allows for visualisations to be made

        Args:
            state (int): the state to perform the action in
            action (Action): the action to evaluate

        Raises:
            NotImplementedError: If this method has not been overridden by
                concrete agent.

        Returns:
            float: the agents interpretation of the value of this state and
            action
        """
        self.__throw_not_implemented()
        return 0

    def __throw_not_implemented(self):
        raise NotImplementedError(
            "This method must be overridden by concrete agent"
        )
