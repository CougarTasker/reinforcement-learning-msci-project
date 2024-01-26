from typing import List

from src.controller.user_action_bridge import UserActionMessage
from src.model.learning_system.learning_system import LearningSystem

from .auto_progress_handler import AutoHandler
from .base_handler import BaseUserActionHandler, HandleResult
from .progress_handler import ProgressHandler
from .set_options_handler import SetOptionsHandler
from .standard_handler import StandardRequestHandler


class UserActionResponsibilityChain(object):
    """This class represents a whole chain of connected handlers."""

    def __init__(self, learning_system: LearningSystem) -> None:
        """Initialise the learning chain.

        Args:
            learning_system (LearningSystem): the model this chain should
                interact with.
        """
        self.learning_system = learning_system

        self.chain: List[BaseUserActionHandler] = [
            StandardRequestHandler(learning_system),
            SetOptionsHandler(learning_system),
            ProgressHandler(learning_system),
            AutoHandler(learning_system),
        ]

    def handle_inaction(self) -> bool:
        """Perform busy waiting when there has not been an action from the user.

        Returns:
            bool: weather there has been an action performed.
        """
        has_been_handled = False
        for user_action_handler in self.chain:
            handle_result = user_action_handler.handle_inaction()
            has_been_handled = has_been_handled or (
                handle_result is HandleResult.success
            )
        return has_been_handled

    def handle_user_action(self, action: UserActionMessage) -> None:
        """Handle a user action with each handler in turn.

        Args:
            action (UserActionMessage): the action from the user.

        Raises:
            RuntimeError: If unable to handle the action provided.
        """
        for user_action_handler in self.chain:
            handle_result = user_action_handler.handle_action(action)
            if handle_result is HandleResult.success:
                return

        raise RuntimeError("unable to handle user action.")
