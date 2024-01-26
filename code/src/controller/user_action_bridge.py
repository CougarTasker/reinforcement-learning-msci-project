from enum import Enum
from typing import Any, Optional

from .base_bridge import BaseBridge


class UserAction(Enum):
    """Enumerate all possible user actions."""

    progress = 0
    select_auto = 1
    reset_state = 2
    fetch_current_state = 3
    set_display_mode = 4
    set_agent = 5
    set_dynamics = 6
    set_agent_strategy = 7
    reset_system = 8
    end = 9


class UserActionMessage(object):
    """Encapsulates a user action and its data."""

    def __init__(self, action: UserAction, payload: Any = None) -> None:
        """Create a user action object.

        Args:
            action (UserAction): the action to be performed
            payload (Any): any related data
        """
        self.action = action
        self.payload = payload


class UserActionBridge(BaseBridge):
    """Bridge for passing the user actions from the view to the model."""

    def submit_action(self, action: UserAction, payload: Any = None):
        """Submit an action to be processed.

        Args:
            action (UserAction): the action the user has performed.
            payload (Any): the data to send, defaults to None.
        """
        self.add_item(UserActionMessage(action, payload))

    def get_action(self) -> UserActionMessage:
        """Get the latest action the user has performed.

        This is blocking.

        Returns:
            UserActionMessage: the action that has been performed
        """
        return self.get_item_blocking()

    def get_action_non_blocking(self) -> Optional[UserActionMessage]:
        """Get the latest action the user has performed.

        This is blocking.

        Returns:
            UserActionMessage: the action that has been performed
        """
        return self.get_item_non_blocking()
