from typing import Optional

from PySide6.QtWidgets import QComboBox, QWidget

from src.controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.report_state_publisher import BaseReportObserver


class ReportSelector(QComboBox, BaseReportObserver):
    """Widget to allow the user to select a hyper parameter for analysis."""

    def __init__(
        self,
        parent: Optional[QWidget],
        report_controller: ReportGeneratorController,
    ) -> None:
        """Initialise the report selector.

        Args:
            parent (Optional[QWidget]): the parent of this widget.
            report_controller (ReportGeneratorController): the controller to
                notify when the user selects a different report..
        """
        super().__init__(parent)

        hyper_parameters = TuningInformation.tunable_parameters()
        self.controller = report_controller
        self.options = {
            TuningInformation.get_parameter_details(parameter).name: parameter
            for parameter in hyper_parameters
        }

        self.addItems(list(self.options.keys()))

        self.currentTextChanged.connect(self.update_handler)

    def update_handler(self, text: str) -> None:
        """Handle update, send the appropriate request to the controller.

        Args:
            text (str): the option that has been selected.
        """
        self.controller.report_request_bridge.request_report(self.options[text])
