from PySide6.QtWidgets import QPushButton, QWidget
from typing_extensions import override

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.model.hyperparameters.hyper_parameter_system import HyperParameterState
from src.view.report_state_publisher import BaseReportObserver


class SearchStartButton(QPushButton, BaseReportObserver):
    """Button to control the starting and stopping of a random search."""

    start_text = "start"
    stop_text = "stop"

    def __init__(
        self,
        parent: QWidget,
        controller: HyperParameterController,
    ):
        """Initialise the start button.

        Args:
            parent (QWidget): the parent this widget should be a part of.
            controller (HyperParameterController): the controller to update
                when pressed.
        """
        self.start_search = True
        super().__init__(self.start_text, parent)
        self.controller = controller

        self.clicked.connect(self.__click_handler)

    @override
    def report_state_updated(self, state: HyperParameterState) -> None:
        """Update the buttons function when the mode changes.

        Args:
            state (HyperParameterState): the new state.
        """
        start_search = not state.search.searching
        if start_search == self.start_text:
            return
        self.start_search = start_search
        new_text = self.start_text if start_search else self.stop_text
        self.setText(new_text)

    def __click_handler(self):
        self.controller.request_bridge.set_search_state(self.start_search)
