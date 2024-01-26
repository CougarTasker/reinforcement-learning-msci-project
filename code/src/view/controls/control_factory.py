from typing import Any, Dict, Optional

from PySide6.QtWidgets import QWidget

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.view.controls.custom_button_widget import (
    CustomButtonWidget,
    responsive_text_handler_type,
)
from src.view.controls.custom_combo_widget import (
    ComboWidgetState,
    CustomComboWidget,
    handler_type,
)
from src.view.state_publisher import StatePublisher


class ControlFactory(object):
    """Factory class for creating controls."""

    def __init__(
        self,
        controller: LearningSystemController,
        state_update_publisher: StatePublisher,
    ) -> None:
        """Initialise the factory.

        Args:
            controller (LearningSystemController): the controller these controls
                should be connected to.
            state_update_publisher (StatePublisher): the publisher used by
                reactive controls.
        """
        self.controller = controller
        self.state_update_publisher = state_update_publisher

    def create_button(
        self,
        parent: QWidget,
        text: str,
        action: UserAction,
        responsive_text_handler: Optional[responsive_text_handler_type] = None,
    ) -> CustomButtonWidget:
        """Create the Button widget.

        Args:
            parent (QWidget): the parent of this widget
            text (str): the text to display
            action (UserAction): the action this button should perform when
                pressed.
            responsive_text_handler (Optional[responsive_text_handler_type]): an
                additional property that can be provided to update the text
                dynamically.

        Returns:
            CustomButtonWidget: the connected widget.
        """
        widget = CustomButtonWidget(parent, text, action, self.controller)

        if responsive_text_handler is not None:
            widget.set_responsive_handler(responsive_text_handler)
            self.state_update_publisher.subscribe(widget)
        return widget

    def create_combo(
        self,
        parent: QWidget,
        options: Dict[str, Any],
        action: UserAction,
        responsive_options_handler: Optional[handler_type] = None,
    ) -> CustomComboWidget:
        """Create combo box widget.

        Args:
            parent (QWidget): the parent widget this widget should be rendered
                into.
            options (Dict[str, Any]): the options to pick between.
            action (UserAction): The user action this combo box corresponds to
            responsive_options_handler (Optional[handler_type]): an optional
                handler to make this combo box responsive to state updates.

        Returns:
            CustomComboWidget: the connected widget.
        """
        first_option = list(options)[0]

        state = ComboWidgetState(options, first_option, enabled=True)
        widget = CustomComboWidget(parent, state, action, self.controller)
        if responsive_options_handler is not None:
            widget.set_responsive_options_handler(responsive_options_handler)
            self.state_update_publisher.subscribe(widget)

        return widget
