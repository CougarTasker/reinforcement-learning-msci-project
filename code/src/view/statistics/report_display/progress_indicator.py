from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QProgressBar, QWidget
from typing_extensions import override

from src.model.hyperparameters.report_data import ReportState
from src.view.report_state_publisher import BaseReportObserver


class ProgressIndicator(QWidget, BaseReportObserver):
    """This widget displays to the user the current progress of the report."""

    progress_bar_steps = 100

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Initialise the report progress indicator.

        Args:
            parent (Optional[QWidget]): the parent of the report progress
                indicator.
        """
        super().__init__(parent)

        layout = QGridLayout(self)

        label = QLabel("Report Generation Progress...")
        layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignBottom)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, self.progress_bar_steps)
        layout.addWidget(self.progress_bar, 1, 0, Qt.AlignmentFlag.AlignTop)

    @override
    def report_state_updated(self, state: ReportState) -> None:
        """Handle when the report progress is updated.

        Args:
            state (ReportState): the new state encompassing the current progress
        """
        report = state.current_report
        if report is None:
            return
        progress = state.pending_requests.get(report, None)
        if progress is None:
            return

        self.progress_bar.setValue(int(self.progress_bar_steps * progress))
