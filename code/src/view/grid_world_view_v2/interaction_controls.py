from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QWidget,
)

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.view.grid_world_view_v2.auto_speed_state_manager import (
    AutoSpeed,
    AutoStateManager,
)


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
        "Manual": AutoSpeed.manual,
        "Auto": AutoSpeed.auto_local,
        "Fast": AutoSpeed.auto_full,
    }

    group_title = "Simulation Interaction Controls"

    def __init__(
        self, parent: QWidget, controller: LearningSystemController
    ) -> None:
        """Initialise the controls.

        Args:
            parent (QWidget): the parent of this widget.
            controller (LearningSystemController): the channel to notify the
                controller of the users actions.
        """
        super().__init__(self.group_title, parent)

        self.controller = controller

        layout = QGridLayout(self)

        self.__add_display_mode(layout)

        self.__add_reset_button(layout)

        self.__add_auto_speed_toggles(layout)

        self.auto_mode_manger = AutoStateManager(controller)

        self.progress_button = QPushButton(
            self.auto_mode_manger.get_progress_button_text()
        )
        self.progress_button.clicked.connect(self.progress_button_pressed)
        layout.addWidget(self.progress_button, 0, 3)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.controller.user_action_bridge.submit_action(UserAction.reset_state)

    def progress_button_pressed(self):
        """When the next button is presses step the state forward."""
        self.auto_mode_manger.progress_button_pressed()
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def auto_speed_toggled(self, option: str):
        """Handle when new speed is selected.

        Args:
            option (str): the new speed to operate.
        """
        auto_speed = self.auto_speed_options[option]
        self.auto_mode_manger.set_speed(auto_speed)
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def display_mode_toggled(self, option: str):
        """When the display mode option menu is selected.

        Args:
            option (str): the mode selected
        """
        display_mode = self.display_mode_options[option]
        self.controller.user_action_bridge.submit_action(
            UserAction.set_display_mode, display_mode
        )

    def __add_display_mode(self, layout: QGridLayout):
        display_mode = QComboBox()
        display_mode.addItems(list(self.display_mode_options.keys()))
        display_mode.currentTextChanged.connect(self.display_mode_toggled)
        layout.addWidget(display_mode, 0, 0)

    def __add_reset_button(self, layout: QGridLayout):
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_button_pressed)
        layout.addWidget(reset_button, 0, 1)

    def __add_auto_speed_toggles(self, layout: QGridLayout):
        auto_speed = QComboBox()
        auto_speed.addItems(list(self.auto_speed_options.keys()))
        auto_speed.currentTextChanged.connect(self.auto_speed_toggled)
        layout.addWidget(auto_speed, 0, 2)
