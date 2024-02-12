from src.controller.learning_system_controller.user_action_bridge import (
    UserAction,
    UserActionMessage,
)
from src.model.learning_system.global_options import AutomaticOptions

from .base_handler import BaseUserActionHandler, HandleResult


class AutoHandler(BaseUserActionHandler):
    """Handles automatic progress actions."""

    def handle_action(self, user_action: UserActionMessage) -> HandleResult:
        """Handle the select auto actions.

        Args:
            user_action (UserActionMessage): the user action provided

        Returns:
            HandleResult: weather this handler has been able to deal with the
                request.
        """
        if user_action.action is not UserAction.select_auto:
            return HandleResult.fail

        self.set_options(automatic=user_action.payload)

        return HandleResult.success

    def handle_inaction(self) -> HandleResult:
        """Handle when there has not been an action.

        In this case the simulation is free to automatically progress the
        simulation.

        Returns:
            HandleResult: weather the hander has automatically progressed the
            simulation.
        """
        automatic_mode = self.learning_system.options.automatic
        not_playing_auto = (
            automatic_mode is not AutomaticOptions.automatic_playing
        )
        if not_playing_auto:
            return HandleResult.fail

        self.learning_instance.perform_action()

        return HandleResult.success
