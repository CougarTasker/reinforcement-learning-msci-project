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

        Should return:
            Action: the action to take in this state
        """
        raise NotImplementedError(
            "This method must be overridden by concrete agent"
        )

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
        raise NotImplementedError(
            "This method must be overridden by concrete agent"
        )
