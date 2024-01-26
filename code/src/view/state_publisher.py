from typing import Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)


class BaseStateObserver(object):
    """The base class for state observers."""

    def state_updated(self, state: StateDescription) -> None:
        """Handle state update events.

        Args:
            state (StateDescription): the new state

        Raises:
            NotImplementedError: If the method is not overridden by a concrete
                observer.
        """
        self.__throw_not_implemented()

    def __throw_not_implemented(self):
        raise NotImplementedError(
            "This method should be overridden by a concrete observer"
        )


class StatePublisher(object):
    """Publisher class for state updates."""

    def __init__(
        self, parent: QWidget, controller: LearningSystemController
    ) -> None:
        """Initialise a new state publisher.

        Args:
            parent (QWidget): the widget that this publisher is associated with.
                timers do not work without this.
            controller (LearningSystemController): the controller to listen for
                state update from.
        """
        timer = QTimer(parent)
        timer.timeout.connect(self.check_for_updates)
        timer.start(1)

        self.update_bridge = controller.state_update_bridge

        self.observers: list[BaseStateObserver] = []

        # used to provided initial state
        self.latest_state: Optional[StateDescription] = None

        # start updates
        controller.user_action_bridge.submit_action(
            UserAction.fetch_current_state
        )

    def subscribe(self, observer: BaseStateObserver) -> None:
        """Subscribe a new observer to state updates.

        Args:
            observer (BaseStateObserver): the observer to listen for state
                updates.
        """
        self.observers.append(observer)
        if self.latest_state is not None:
            observer.state_updated(self.latest_state)

    def check_for_updates(self):
        """Check if any updates to the UI are requested."""
        state = self.update_bridge.get_latest_state()
        if state is not None:
            for observer in self.observers:
                observer.state_updated(state)
