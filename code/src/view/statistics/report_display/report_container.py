from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QStackedWidget, QWidget
from typing_extensions import override

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.model.hyperparameters.hyper_parameter_system import HyperParameterState
from src.view.report_state_publisher import (
    BaseReportObserver,
    ReportStatePublisher,
)
from src.view.statistics.report_display.progress_indicator import (
    ProgressIndicator,
)
from src.view.statistics.report_display.report_information_display import (
    ReportInformationDisplay,
)
from src.view.statistics.report_display.report_selector import ReportSelector


class ReportContainer(QWidget):
    """Widget for displaying a hyper parameter report."""

    def __init__(
        self,
        parent: Optional[QWidget],
        report_controller: HyperParameterController,
        publisher: ReportStatePublisher,
    ) -> None:
        """Initialise the report display widget.

        uses matplotlib to create graphs.

        Args:
            parent (Optional[QWidget]): the parent of this widget.
            report_controller (HyperParameterController): the controller to
                interact with the report information.
            publisher (ReportStatePublisher): the publisher that notifies the
                report to updates.

        """
        super().__init__(parent)

        self.layout_manager = QGridLayout(self)

        selector = ReportSelector(self, report_controller)
        self.layout_manager.addWidget(selector, 0, 0)
        publisher.subscribe(selector)

        self.main_widget_area = MainWidgetSwitcher(self, publisher)
        self.layout_manager.addWidget(self.main_widget_area, 1, 0)


class MainWidgetSwitcher(QStackedWidget, BaseReportObserver):
    """Widget that switches to the appropriate display for the current state."""

    def __init__(
        self, parent: Optional[QWidget], publisher: ReportStatePublisher
    ) -> None:
        """Initialise the widget switcher.

        Args:
            parent (Optional[QWidget]): the parent of this widget
            publisher (ReportStatePublisher): the publisher providing the update
                events that drive this switcher.
        """
        super().__init__(parent)

        placeholder_text = QLabel("Select parameter to analyse.")
        placeholder_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(placeholder_text)

        self.progress_bar = ProgressIndicator(self)
        self.addWidget(self.progress_bar)
        publisher.subscribe(self.progress_bar)

        self.information_display = ReportInformationDisplay(self)
        self.addWidget(self.information_display)
        publisher.subscribe(self.information_display)

        publisher.subscribe(self)

    @override
    def report_state_updated(self, state: HyperParameterState) -> None:
        """Update the figure when a new report is provided.

        Args:
            state (HyperParameterState): the new report information.
        """
        report = state.report
        report_parameter = report.current_report
        if report_parameter is None:
            return

        if report_parameter in report.pending_requests:
            self.setCurrentWidget(self.progress_bar)

        if report_parameter in report.available_reports:
            self.setCurrentWidget(self.information_display)
