from PySide6.QtWidgets import QGridLayout, QGroupBox, QWidget

from src.controller.learning_system_controller.user_action_bridge import (
    UserAction,
)
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.global_options import AutomaticOptions
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.controls.control_factory import ControlFactory


class InteractionControls(QGroupBox):
    """Widget that contains the controls for interacting with the grid world."""

    display_mode_options = {
        "default": DisplayMode.default,
        "best action": DisplayMode.best_action,
        "state value": DisplayMode.state_value,
        "action value": DisplayMode.action_value_global,
        "action value local": DisplayMode.action_value_local,
    }

    auto_speed_options = {
        "Manual": AutomaticOptions.manual,
        "Auto": AutomaticOptions.automatic_playing,
    }

    reset_button_text = "Reset"

    group_title = "Simulation Interaction Controls"

    progress_button_text = {
        AutomaticOptions.manual: "Next",
        AutomaticOptions.automatic_playing: "Pause",
        AutomaticOptions.automatic_paused: "Play",
    }

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
            self, self.display_mode_options, UserAction.set_display_mode
        )
        layout.addWidget(display_mode, 0, 0)

        reset_button = control_factory.create_button(
            self, self.reset_button_text, UserAction.reset_state
        )
        layout.addWidget(reset_button, 0, 1)

        auto_mode = control_factory.create_combo(
            self, self.auto_speed_options, UserAction.select_auto
        )
        layout.addWidget(auto_mode, 0, 2)

        progress_button = control_factory.create_button(
            self,
            self.progress_button_text[AutomaticOptions.manual],
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
        return self.progress_button_text[state.global_options.automatic]
