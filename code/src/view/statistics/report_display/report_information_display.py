from typing import Optional

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.report_data import ReportState
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.report_state_publisher import BaseReportObserver
from src.view.statistics.matplotlib_setup import create_canvas


class ReportInformationDisplay(QWidget, BaseReportObserver):
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

        figure = Figure()
        self.canvas = create_canvas(figure)

        layout.addWidget(self.canvas, 0, 0)

        axes = figure.subplots()
        if not isinstance(axes, Axes):
            raise RuntimeError("Incorrect axis object")

        self.axes = axes
        self.current_parameter: Optional[HyperParameter] = None

    @override
    def report_state_updated(self, state: ReportState) -> None:
        """Handle when the report progress is updated.

        Args:
            state (ReportState): the new state encompassing the current progress
        """
        report_parameter = state.current_report
        if report_parameter is None:
            return
        if report_parameter is self.current_parameter:
            return
        self.current_parameter = report_parameter
        report_data = state.available_reports.get(report_parameter, None)
        if report_data is None:
            return

        details = TuningInformation.get_parameter_details(report_parameter)

        self.__reset_plot(details.get_display_name())

        self.axes.plot(report_data.x_axis, report_data.y_axis, "b-")

        best_index = np.argmax(report_data.y_axis)
        best_value = report_data.x_axis[best_index]
        best_result = report_data.y_axis[best_index]

        self.axes.plot([best_value], [best_result], "r*")
        self.axes.annotate(
            f"({best_value:.3g}, {best_result:.3g})",
            (best_value, best_result),
        )
        self.canvas.draw()

    def __reset_plot(self, name: str):
        self.axes.clear()
        self.axes.set_xlabel(f"{name} Value")
        self.axes.set_ylabel("Total Reward")
        self.axes.set_title(f"{name} vs Total Reward")
