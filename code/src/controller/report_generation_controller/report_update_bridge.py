from typing import Optional

from src.model.hyperparameters.report_data import ReportState

from ..base_bridge import BaseBridge


class ReportUpdateBridge(BaseBridge):
    """Bridge for passing report updates to the view."""

    def update_report_state(self, state: ReportState):
        """Set the new state to be displayed.

        Args:
            state (ReportState): The new report state.
        """
        self.add_item(state)

    def get_latest_state(self) -> Optional[ReportState]:
        """Get the last (most recent) new report state.

        Returns:
            Optional[ReportState]: the new state, none if there has been no
                change.
        """
        latest_state = None
        state = self.get_item_non_blocking()
        while state is not None:
            latest_state = state
            state = self.get_item_non_blocking()
        return latest_state
