from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from src.model.hyperparameters.report_data import (
    HyperParameterReport,
    ReportState,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.report_state_publisher import (
    BaseReportObserver,
    ReportStatePublisher,
)
from src.view.statistics.matplotlib_setup import create_canvas
from src.view.statistics.report_selector import ReportSelector


class ReportDisplay(QWidget, BaseReportObserver):
    """Widget for displaying a hyper parameter report."""

    def __init__(
        self,
        parent: Optional[QWidget],
        report_controller: ReportGeneratorController,
    ) -> None:
        """Initialise the report display widget.

        uses matplotlib to create graphs.

        Args:
            parent (Optional[QWidget]): the parent of this widget
            report_controller (ReportGeneratorController): the controller to
                interact with the report information.

        Raises:
            RuntimeError: If there is an issue with matplotlib.
        """
        super().__init__(parent)

        layout = QGridLayout(self)

        selector = ReportSelector(self, report_controller)
        layout.addWidget(selector, 0, 0)

        self.figure = Figure()
        self.canvas = create_canvas(self.figure)
        layout.addWidget(self.canvas, 1, 0)
        axes = self.figure.subplots()
        if not isinstance(axes, Axes):
            raise RuntimeError("Incorrect axis object")

        self.axes = axes
        self.current_report: Optional[HyperParameterReport] = None

        self.publisher = ReportStatePublisher(self, report_controller)
        self.publisher.subscribe(self)

    @override
    def report_state_updated(self, state: ReportState) -> None:
        """Update the figure when a new report is provided.

        Args:
            state (ReportState): the new report information.
        """
        report = state.current_report
        if report is None:
            return
        details = TuningInformation.get_parameter_details(report)
        self.__reset_plot(details.get_display_name())

        report_data = state.available_reports.get(report, None)
        if report_data == self.current_report:
            return
        self.current_report = report_data

        if report_data is None:
            return

        self.axes.plot(
            report_data.x_axis,
            report_data.y_axis,
        )
        self.canvas.draw()

    def __reset_plot(self, name: str):
        self.axes.clear()
        self.axes.set_xlabel(f"{name} Value")
        self.axes.set_ylabel("Total Reward")
        self.axes.set_title(f"{name} vs Total Reward")
