from ...config.agent_section import AgentConfig
from ...dynamics.actions import Action
from ..base_agent import BaseAgent


class QLearningAgent(BaseAgent):
    """Agent that learns q-value table to make decisions."""

    def __init__(
        self,
        config: AgentConfig,
    ) -> None:
        """Initialise the agent.

        Args:
            config (AgentConfig): the configuration for the agent.
        """
        super().__init__(config)

        self.discount_rate = config.discount_rate()

    def get_state_action_value(self, state: int, action: Action) -> float:
        """Get the agents interpretation value of a given state-action.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to get the value of

        Returns:
            float: the expected value for this state and action
        """
        return 0

    def get_state_value(self, state: int) -> float:
        """Get the agents interpretation of the value of this state.

        Args:
            state (int): the state to evaluate

        Returns:
            float: the agents interpretation of the value of this state
        """
        return 0

    def evaluate_policy(self, state: int) -> Action:
        """Decide on the action this agent would take in a given state.

        picks the best action based upon the value table.

        Args:
            state (int): the state the agent is performing this action


        Returns:
            Action: the action to take in this state
        """
        return Action.up

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

        """
        # not used yet
