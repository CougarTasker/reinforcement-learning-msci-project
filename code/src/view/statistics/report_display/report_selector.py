from typing import Dict, List, Optional

from PySide6.QtWidgets import QComboBox, QWidget
from typing_extensions import override

from src.controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.report_data import ReportState
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.report_state_publisher import BaseReportObserver


class ReportSelector(QComboBox, BaseReportObserver):
    """Widget to allow the user to select a hyper parameter for analysis."""

    none_selected_text = "None Selected"

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

        self.reset_guard = False

        self.currentTextChanged.connect(self.update_handler)
        self.current_items: List[str] = []

    def update_handler(self, text: str) -> None:
        """Handle update, send the appropriate request to the controller.

        Args:
            text (str): the option that has been selected.
        """
        if self.reset_guard:
            return
        if text is self.none_selected_text:
            return
        self.controller.report_request_bridge.request_report(self.options[text])

    @override
    def report_state_updated(self, state: ReportState) -> None:
        """Update the figure when a new report is provided.

        Args:
            state (ReportState): the new report information.
        """
        self.reset_guard = True

        update_options: Dict[Optional[HyperParameter], str] = {
            option: name for name, option in self.options.items()
        }
        if state.current_report is None:
            update_options[None] = self.none_selected_text

        new_items = list(update_options.values())
        # avoid redundant updates can cause flickering
        if new_items != self.current_items:
            self.clear()
            self.addItems(new_items)
            self.current_items = new_items

        new_current_text = update_options[state.current_report]
        if self.currentText() != new_current_text:
            self.setCurrentText(new_current_text)
        self.reset_guard = False
