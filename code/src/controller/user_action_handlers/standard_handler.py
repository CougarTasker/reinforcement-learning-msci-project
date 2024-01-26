from src.controller.user_action_bridge import UserAction, UserActionMessage
from src.controller.user_action_handlers.base_handler import (
    BaseUserActionHandler,
    HandleResult,
)


class StandardRequestHandler(BaseUserActionHandler):
    """Handles requests that dont involve any processing."""

    def handle_action(self, user_action: UserActionMessage) -> HandleResult:
        """Handle the actions that involve simple requests.

        Args:
            user_action (UserActionMessage): the user action provided

        Returns:
            HandleResult: weather this handler has been able to deal with the
                request.
        """
        match user_action:
            case UserActionMessage(action=UserAction.reset_state):
                self.learning_instance.reset_state()
            case UserActionMessage(action=UserAction.fetch_current_state):
                # no precessing necessary
                return HandleResult.success
            case UserActionMessage(action=UserAction.reset_system):
                self.learning_system.reset_top_level()
            case _:
                return HandleResult.fail

        return HandleResult.success
