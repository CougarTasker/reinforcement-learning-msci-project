from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from PySide6.QtWidgets import QComboBox, QWidget
from typing_extensions import override

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.state_publisher import BaseStateObserver


@dataclass(frozen=True)
class ComboWidgetState(object):
    """Class that represents the configuration of a combo box."""

    options: Dict[str, Any]
    selected_option: str
    enabled: bool = True


handler_type = Callable[[StateDescription], ComboWidgetState]


class CustomComboWidget(QComboBox, BaseStateObserver):
    """Extension of a combo box widget to provide update functionality."""

    def __init__(
        self,
        parent: QWidget,
        state: ComboWidgetState,
        action: UserAction,
        controller: LearningSystemController,
    ) -> None:
        """Initialise the combo box widget.

        Args:
            parent (QWidget): the parent widget this widget should be rendered
                into.
            state (ComboWidgetState): The configuration of the combo box.
            action (UserAction): The user action this combo box corresponds to
            controller (LearningSystemController): the controller to update when
                the user selects something.
        """
        super().__init__(parent)
        self.state = state
        self.__set_state(state)
        self.action = action
        self.controller = controller

        self.responsive_options_handler: Optional[handler_type] = None

        self.currentTextChanged.connect(self.__update_handler)

    def set_responsive_options_handler(
        self, responsive_options_handler: handler_type
    ):
        """Set the handler for responsive options.

        Args:
            responsive_options_handler (handler_type): he method
                for generating the options.
        """
        self.responsive_options_handler = responsive_options_handler

    @override
    def state_updated(self, state: StateDescription) -> None:
        """Handle state update events.

        Args:
            state (StateDescription): the new state
        """
        if self.responsive_options_handler is not None:
            combo_state = self.responsive_options_handler(state)
            self.__set_state(combo_state)

    def __update_handler(self, text: str) -> None:
        """Handle update, send the appropriate request to the user.

        Args:
            text (str): the option that has been selected.
        """
        self.controller.user_action_bridge.submit_action(
            self.action, self.state.options[text]
        )

    def __set_state(self, state: ComboWidgetState):
        self.state = state
        self.addItems(list(state.options.keys()))
        self.setCurrentText(state.selected_option)
        self.setEnabled(state.enabled)
