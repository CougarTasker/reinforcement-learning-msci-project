from typing import Callable, Optional

from PySide6.QtWidgets import QPushButton, QWidget
from typing_extensions import override

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.state_publisher import BaseStateObserver

responsive_text_handler_type = Callable[[StateDescription], str]


class CustomButtonWidget(QPushButton, BaseStateObserver):
    """Custom Button widget configured to update the controller."""

    def __init__(
        self,
        parent: QWidget,
        text: str,
        action: UserAction,
        controller: LearningSystemController,
    ):
        """Initialise the Button widget.

        Args:
            parent (QWidget): the parent of this widget
            text (str): the text to display
            action (UserAction): the action this button should perform when
                pressed.
            controller (LearningSystemController): the controller to notify.
        """
        super().__init__(text, parent)
        self.action = action
        self.controller = controller

        self.clicked.connect(self.__click_handler)

        self.responsive_text_handler: Optional[
            responsive_text_handler_type
        ] = None

    def set_responsive_handler(
        self, responsive_text_handler: responsive_text_handler_type
    ):
        """Set the handler for responsive text.

        Args:
            responsive_text_handler (responsive_text_handler_type): the method
                for generating the buttons text.
        """
        self.responsive_text_handler = responsive_text_handler

    @override
    def state_updated(self, state: StateDescription) -> None:
        """Handle state update events.

        Args:
            state (StateDescription): the new state
        """
        if self.responsive_text_handler is not None:
            text = self.responsive_text_handler(state)
            self.setText(text)

    def __click_handler(self) -> None:
        """Update the controller when a click is registered."""
        self.controller.user_action_bridge.submit_action(self.action)
