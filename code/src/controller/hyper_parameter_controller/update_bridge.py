from typing import Optional

from src.model.hyperparameters.hyper_parameter_system import HyperParameterState

from ..base_bridge import BaseBridge


class HyperParameterUpdateBridge(BaseBridge):
    """Bridge for passing report updates to the view."""

    def update_state(self, state: HyperParameterState):
        """Set the new state to be displayed.

        Args:
            state (HyperParameterState): The new hyper parameter state.
        """
        self.add_item(state)

    def get_latest_state(self) -> Optional[HyperParameterState]:
        """Get the last (most recent) new report state.

        Returns:
            Optional[HyperParameterState]: the new state, none if there has not
                been any changes.
        """
        latest_state = None
        state = self.get_item_non_blocking()
        while state is not None:
            latest_state = state
            state = self.get_item_non_blocking()
        return latest_state
