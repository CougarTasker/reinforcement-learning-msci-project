from typing import Optional

from PySide6.QtWidgets import QTabWidget, QWidget

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.view.display_state_v2.display import DisplayState
from src.view.report_state_publisher import ReportStatePublisher
from src.view.state_publisher import StatePublisher
from src.view.statistics.report_display.report_container import ReportContainer
from src.view.statistics.reward_history import RewardHistory
from src.view.statistics.search_results.container import SearchDisplay


class MainTabArea(QTabWidget):
    """Tab widget to contain the main content areas."""

    def __init__(
        self,
        parent: Optional[QWidget],
        state_publisher: StatePublisher,
        report_controller: HyperParameterController,
    ) -> None:
        """Initialise the tab widget.

        Args:
            parent (Optional[QWidget]): the parent of the tab widget.
            state_publisher (StatePublisher): the state publisher for the live
                updating tabs.
            report_controller (HyperParameterController): the controller for
                the report display tab.
        """
        super().__init__(parent)

        display_state = DisplayState(None)
        state_publisher.subscribe(display_state)
        self.addTab(display_state, "Current State")

        reward_history = RewardHistory(None)
        state_publisher.subscribe(reward_history)
        self.addTab(reward_history, "Reward History")

        self.publisher = ReportStatePublisher(self, report_controller)

        search_display = SearchDisplay(None, report_controller, self.publisher)
        self.addTab(search_display, "Hyper-Parameter Search")

        report_display = ReportContainer(
            None, report_controller, self.publisher
        )
        self.addTab(report_display, "Hyper-Parameter Tuning")
