from typing import Optional

from src.model.learning_system.state_description import StateDescription

from .base_bridge import BaseBridge


class StateUpdateBridge(BaseBridge):
    """Bridge for passing state updates to the view."""

    def update_state(self, state: StateDescription):
        """Set the new state to be displayed.

        Args:
            state (StateDescription): The new state.
        """
        self.queue.put_nowait(state)

    def get_latest_state(self) -> Optional[StateDescription]:
        """Get the last (most recent) new state.

        Returns:
            Optional[StateDescription]: the new state, none if none has been set
        """
        last_state: Optional[StateDescription] = None
        while not self.queue.empty():
            last_state = self.queue.get_nowait()
        return last_state
