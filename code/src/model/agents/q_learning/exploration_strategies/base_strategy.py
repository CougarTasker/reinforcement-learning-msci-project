from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.actions import Action
from src.model.transition_information import TransitionInformation


class BaseExplorationStrategy(object):
    """Provides the common base for different exploration strategies."""

    def __init__(self, agent: BaseAgent) -> None:
        """Initialise the Exploration strategy.

        Args:
            agent (BaseAgent): The agent that uses this strategy.
        """
        self.agent = agent

    def select_action(self, state: int) -> Action:
        """Select the action based upon this strategy.

        Args:
            state (int): the state where this action will be performed

        Raises:
            NotImplementedError: If this method has not been overridden by a
                concrete strategy.

        Returns:
            Action: The action the agent should perform
        """
        self.__throw_not_implemented()
        return Action.up

    def record_transition(self, transition: TransitionInformation) -> None:
        """Provide the strategy with the information from a transition.

        Args:
            transition (TransitionInformation): The transition information.

        """
        # not implemented

    def __throw_not_implemented(self):
        raise NotImplementedError(
            "This method must be overridden by concrete strategy"
        )
