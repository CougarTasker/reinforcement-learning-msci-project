from typing import Optional

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget
from typing_extensions import override

from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.state_publisher import BaseStateObserver


class BaseVisibilityObserver(QWidget, BaseStateObserver):
    """Class that should observe state updates only while visible.

    This class avoids wasted work on updates that might not be visible.
    """

    def __init__(self, parent: QWidget | None) -> None:
        """Initialise the observer.

        Args:
            parent (QWidget | None): The parent widget.
        """
        super().__init__(parent)

        self._missing_ui_state_update: Optional[StateDescription] = None

    @override
    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802
        """Handle the show event, necessary if there have been missed updates.

        Args:
            event (QShowEvent): the show event information.
        """
        if self._missing_ui_state_update is not None:
            self.visible_state_updated(self._missing_ui_state_update)
            self._missing_ui_state_update = None
        super().showEvent(event)

    def state_updated(self, state: StateDescription) -> None:
        """Handle the state update event.

        Args:
            state (StateDescription): the new state.
        """
        if self.isVisible():
            self.visible_state_updated(state)
        else:
            self._missing_ui_state_update = state

    def visible_state_updated(self, state: StateDescription) -> None:
        """Handle the state update only when visible.

        Args:
            state (StateDescription): the new state.

        Raises:
            NotImplementedError: if the method is not overridden in the concrete
                class.
        """
        raise NotImplementedError("Not implemented")
