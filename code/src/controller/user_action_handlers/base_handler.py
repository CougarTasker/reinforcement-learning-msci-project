from dataclasses import replace
from enum import Enum

from src.controller.user_action_bridge import UserActionMessage
from src.model.learning_system.learning_instance import LearningInstance
from src.model.learning_system.learning_system import LearningSystem


class HandleResult(Enum):
    """Enumerates how a handler has performed."""

    success = 0
    fail = 1


class BaseUserActionHandler(object):
    """Base class for user action handlers."""

    def __init__(
        self,
        learning_system: LearningSystem,
    ) -> None:
        """Initialise the handler.

        Args:
            learning_system (LearningSystem): The system to interact with.
        """
        self.learning_system = learning_system

    def handle_action(self, user_action: UserActionMessage) -> HandleResult:
        """Handle the users action. Concrete handlers should override this.

        If the hander is not successful it will be passed onto the next in the
        chain.

        Args:
            user_action (UserActionMessage): the action the handler
                should consider.

        Returns:
            HandleResult: weather this handler has been successful.
        """
        return HandleResult.fail

    def handle_inaction(self) -> HandleResult:
        """Handle if there has not been an action provided.

        Returns:
            HandleResult: weather this handler has been successful.
        """
        return HandleResult.fail

    @property
    def learning_instance(self) -> LearningInstance:
        """Get the learning instance.

        Returns:
            LearningInstance: the learning instance to interact with.
        """
        return self.learning_system.learning_instance

    def set_options(self, **options):
        """Shorthand for updating global options.

        Args:
            options (Dict[str, Any]): the options to change.
        """
        self.learning_system.update_options(
            replace(self.learning_system.options, **options)
        )

    def set_top_level_options(self, **options):
        """Shorthand for updating entity options.

        Args:
            options (Dict[str, Any]): the options to change.
        """
        existing_options = self.learning_system.options
        top_level_options = replace(
            existing_options.top_level_options,
            **options,
        )

        self.learning_system.update_options(
            replace(
                existing_options,
                top_level_options=top_level_options,
            )
        )
