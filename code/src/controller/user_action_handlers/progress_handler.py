from src.controller.user_action_bridge import UserAction, UserActionMessage
from src.controller.user_action_handlers.base_handler import (
    BaseUserActionHandler,
    HandleResult,
)
from src.model.learning_system.options import AutomaticOptions


class ProgressHandler(BaseUserActionHandler):
    """Handles the progress button action.

    this action is contextual on the current state of the model: weather the
    system is operating automatically.
    """

    def handle_action(self, user_action: UserActionMessage) -> HandleResult:
        """Handle the progress action.

        Args:
            user_action (UserActionMessage): the user action provided

        Returns:
            HandleResult: weather this handler has been able to deal with the
                request.
        """
        if user_action.action is not UserAction.progress:
            return HandleResult.fail

        match self.learning_system.options.automatic:
            case AutomaticOptions.manual:
                self.learning_instance.perform_action()
            case AutomaticOptions.automatic_paused:
                self.set_options(automatic=AutomaticOptions.automatic_playing)
            case AutomaticOptions.automatic_playing:
                self.set_options(automatic=AutomaticOptions.automatic_paused)
            case _:
                return HandleResult.fail

        return HandleResult.success
