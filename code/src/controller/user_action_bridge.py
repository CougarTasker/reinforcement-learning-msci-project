from enum import Enum
from typing import Any

from .base_bridge import BaseBridge


class UserAction(Enum):
    """Enumerate all possible user actions."""

    one_step = 0
    start_auto = 1
    stop_auto = 2
    reset = 3
    fetch_current_state = 4
    set_display_mode = 5


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
        self.queue.put_nowait(UserActionMessage(action, payload))

    def has_new_action(self) -> bool:
        """Is there a new action to process.

        Returns:
            bool: true when there is another action to consider.
        """
        return not self.queue.empty()

    def get_action(self) -> UserActionMessage:
        """Get the latest action the user has performed.

        This is blocking.

        Returns:
            UserActionMessage: the action that has been performed
        """
        return self.queue.get()
