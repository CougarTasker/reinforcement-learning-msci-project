from PySide6.QtWidgets import QGridLayout, QGroupBox, QWidget

from src.controller.learning_system_controller.user_action_bridge import (
    UserAction,
)
from src.model.learning_system.global_options import AutomaticOptions
from src.model.learning_system.learning_system import LearningSystem
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.controls.control_factory import ControlFactory
from src.view.controls.custom_combo_widget import ComboWidgetState
from src.view.option_display_text import OptionDisplayText


class InteractionControls(QGroupBox):
    """Widget that contains the controls for interacting with the grid world."""

    reset_button_text = "Reset"

    group_title = "Simulation Interaction Controls"

    def __init__(
        self, parent: QWidget, control_factory: ControlFactory
    ) -> None:
        """Initialise the controls.

        Args:
            parent (QWidget): the parent of this widget.
            control_factory (ControlFactory): the factory to make the controls
                with.
        """
        super().__init__(self.group_title, parent)

        layout = QGridLayout(self)

        display_mode = control_factory.create_combo(
            self,
            ComboWidgetState(
                OptionDisplayText.display_mode_options,
                LearningSystem.initial_global_options.display_mode,
            ),
            UserAction.set_display_mode,
            self.__display_responsive_options,
        )
        layout.addWidget(display_mode, 0, 0)

        reset_button = control_factory.create_button(
            self, self.reset_button_text, UserAction.reset_state
        )
        layout.addWidget(reset_button, 0, 1)

        auto_mode = control_factory.create_combo(
            self,
            ComboWidgetState(
                OptionDisplayText.auto_selector_options,
                LearningSystem.initial_global_options.automatic,
            ),
            UserAction.select_auto,
            self.__auto_responsive_options,
        )
        layout.addWidget(auto_mode, 0, 2)

        progress_button = control_factory.create_button(
            self,
            OptionDisplayText.progress_button_text.get_text(
                LearningSystem.initial_global_options.automatic
            ),
            UserAction.progress,
            self.__progress_button_responsive_text,
        )
        layout.addWidget(progress_button, 0, 3)

    def __progress_button_responsive_text(self, state: StateDescription) -> str:
        """Calculate the responsive text for the next button.

        Args:
            state (StateDescription): the current state.

        Returns:
            str: the string to show on the button.
        """
        return OptionDisplayText.progress_button_text.get_text(
            state.global_options.automatic
        )

    def __auto_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        # limited subset of modes for simplicity.
        mode = (
            AutomaticOptions.manual
            if state.global_options.automatic == AutomaticOptions.manual
            else AutomaticOptions.automatic_playing
        )
        return ComboWidgetState(
            OptionDisplayText.auto_selector_options,
            mode,
        )

    def __display_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        return ComboWidgetState(
            OptionDisplayText.display_mode_options,
            state.global_options.display_mode,
        )
