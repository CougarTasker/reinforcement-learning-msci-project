from typing import Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from src.controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from src.model.hyperparameters.report_data import ReportState


class BaseReportObserver(object):
    """The base class for report state observers."""

    def report_state_updated(self, state: ReportState) -> None:
        """Handle report state update events.

        Args:
            state (ReportState): the new report state

        Raises:
            NotImplementedError: If the method is not overridden by a concrete
                observer.
        """
        self.__throw_not_implemented()

    def __throw_not_implemented(self):
        raise NotImplementedError(
            "This method should be overridden by a concrete observer"
        )


class ReportStatePublisher(object):
    """Publisher class for state updates."""

    def __init__(
        self, parent: QWidget, controller: ReportGeneratorController
    ) -> None:
        """Initialise a new state publisher.

        Args:
            parent (QWidget): the widget that this publisher is associated with.
                timers do not work without this.
            controller (ReportGeneratorController): the controller to listen for
                state update from.
        """
        timer = QTimer(parent)
        timer.timeout.connect(self.check_for_updates)
        # slow update cycle not performance critical
        timer.start(100)

        self.update_bridge = controller.report_update_bridge

        self.observers: list[BaseReportObserver] = []

        # used to provided initial state
        self.latest_state: Optional[ReportState] = None

        # start updates
        controller.report_request_bridge.request_current_state()

    def subscribe(self, observer: BaseReportObserver) -> None:
        """Subscribe a new observer to state updates.

        Args:
            observer (BaseReportObserver): the observer to listen for state
                updates.
        """
        self.observers.append(observer)
        if self.latest_state is not None:
            observer.report_state_updated(self.latest_state)

    def check_for_updates(self):
        """Check if any updates to the UI are requested."""
        state = self.update_bridge.get_latest_state()
        if state is not None:
            for observer in self.observers:
                observer.report_state_updated(state)
