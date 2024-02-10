from typing import Optional

from src.model.learning_system.state_description.state_description import (
    StateDescription,
)

from .base_bridge import BaseBridge


class StateUpdateBridge(BaseBridge):
    """Bridge for passing state updates to the view."""

    def update_state(self, state: StateDescription):
        """Set the new state to be displayed.

        Args:
            state (StateDescription): The new state.
        """
        self.add_item(state)

    def get_latest_state(self) -> Optional[StateDescription]:
        """Get the last (most recent) new state.

        Returns:
            Optional[StateDescription]: the new state, none if none has been set
        """
        latest_state = None
        state = self.get_item_non_blocking()
        while state is not None:
            latest_state = state
            state = self.get_item_non_blocking()
        return latest_state
