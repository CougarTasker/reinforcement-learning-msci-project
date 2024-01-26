from enum import Enum
from typing import Any

from .base_bridge import BaseBridge


class UserAction(Enum):
    """Enumerate all possible user actions."""

    one_step = 0
    start_auto = 1
    stop_auto = 2
    reset_state = 3
    fetch_current_state = 4
    set_display_mode = 5
    set_agent = 6
    set_dynamics = 7
    set_agent_strategy = 8
    reset_system = 9
    end = 10


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

    def get_action_non_blocking(self) -> UserActionMessage:
        """Get the latest action the user has performed.

        This is blocking.

        Returns:
            UserActionMessage: the action that has been performed
        """
        return self.get_item_non_blocking()
