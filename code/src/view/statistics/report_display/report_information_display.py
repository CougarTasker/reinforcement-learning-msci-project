from typing import Optional

from matplotlib.axes import Axes
from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.model.hyperparameters.hyper_parameter_system import HyperParameterState
from src.model.hyperparameters.report_generation.report_data import (
    HyperParameterReport,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.report_state_publisher import BaseReportObserver
from src.view.statistics.plotting import BasePlotter, PlottingCanvas


class ReportInformationDisplay(QWidget, BaseReportObserver, BasePlotter):
    """This widget displays to the user the information from the report."""

    progress_bar_steps = 100

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Initialise the report progress indicator.

        Args:
            parent (Optional[QWidget]): the parent of the report progress
                indicator.

        Raises:
            RuntimeError: If there is an issue with matplotlib.
        """
        super().__init__(parent)

        layout = QGridLayout(self)

        self.canvas = PlottingCanvas(self, self)
        layout.addWidget(self.canvas, 0, 0)

        self.current_report: Optional[HyperParameterReport] = None

    @override
    def report_state_updated(self, state: HyperParameterState) -> None:
        """Handle when the report progress is updated.

        Args:
            state (HyperParameterState): the new state encompassing the current
                progress
        """
        report_parameter = state.report.current_report
        if report_parameter is None:
            return

        report_unchanged = (
            self.current_report is not None
            and report_parameter is self.current_report.parameter
        )

        if report_unchanged:
            return
        report_data = state.report.available_reports.get(report_parameter, None)
        if report_data is None:
            return

        self.current_report = report_data
        self.canvas.request_update()

    @override
    def plot_data(self, axes: Axes):
        """Get the content for the plotting canvas.

        Args:
            axes (Axes): the axes to plot to.
        """
        if self.current_report is None:
            return

        details = TuningInformation.get_parameter_details(
            self.current_report.parameter
        )
        axes.set_title(f"{details.get_display_name()} vs Total Reward")
        axes.set_xlabel(f"{details.get_display_name()} Value")
        axes.set_ylabel("Total Reward")
        axes.fill_between(
            self.current_report.x_axis,
            self.current_report.lower_confidence_bound,
            self.current_report.upper_confidence_bound,
            color="b",
            alpha=0.1 * 3,
        )
        axes.plot(self.current_report.x_axis, self.current_report.y_axis, "r-")
