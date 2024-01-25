from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QPushButton,
    QRadioButton,
    QWidget,
)

from src.controller.user_action_bridge import UserAction, UserActionBridge
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.view.grid_world_view_v2.auto_speed_state_manager import (
    AutoSpeed,
    AutoStateManager,
)


class Controls(QWidget):
    """Widget that contains the controls for interacting with the grid world."""

    display_mode_options = {
        "default": DisplayMode.default,
        "best action": DisplayMode.best_action,
        "state value": DisplayMode.state_value,
        "action value": DisplayMode.action_value_global,
        "action value local": DisplayMode.action_value_local,
    }

    def __init__(
        self, parent: QWidget, action_bridge: UserActionBridge
    ) -> None:
        """Initialise the controls.

        Args:
            parent (QWidget): the parent of this widget.
            action_bridge (UserActionBridge): the channel to notify the
                controller of the users actions.
        """
        super().__init__(parent)

        self.action_bridge = action_bridge

        layout = QGridLayout(self)

        self.__add_display_mode(layout)

        self.__add_reset_button(layout)

        self.__add_auto_speed_toggles(layout)

        self.auto_mode_manger = AutoStateManager(action_bridge)

        self.progress_button = QPushButton(
            self.auto_mode_manger.get_progress_button_text()
        )
        self.progress_button.clicked.connect(self.progress_button_pressed)
        layout.addWidget(self.progress_button, 0, 3)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.action_bridge.submit_action(UserAction.reset)

    def progress_button_pressed(self):
        """When the next button is presses step the state forward."""
        self.auto_mode_manger.progress_button_pressed()
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def auto_speed_toggled(self, speed: AutoSpeed):
        """Handle when new speed is selected.

        Args:
            speed (AutoSpeed): the new speed to operate.
        """
        self.auto_mode_manger.set_speed(speed)
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def display_mode_changed(self, option: str):
        """When the display mode option menu is selected.

        Args:
            option (str): the mode selected
        """
        display_mode = self.display_mode_options[option]
        self.action_bridge.submit_action(
            UserAction.set_display_mode, display_mode
        )

    def __add_display_mode(self, layout: QGridLayout):
        display_mode = QComboBox()
        display_mode.addItems(list(self.display_mode_options.keys()))
        display_mode.currentTextChanged.connect(self.display_mode_changed)
        layout.addWidget(display_mode, 0, 0)

    def __add_reset_button(self, layout: QGridLayout):
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_button_pressed)
        layout.addWidget(reset_button, 0, 1)

    def __add_auto_speed_toggles(self, layout: QGridLayout):
        manual_mode = QRadioButton("Manual", self)
        manual_mode.setChecked(True)
        manual_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.manual)
        )
        layout.addWidget(manual_mode, 0, 2)

        auto_mode = QRadioButton("Auto", self)
        auto_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.auto_local)
        )
        layout.addWidget(auto_mode, 1, 2)

        fast_mode = QRadioButton("Fast", self)
        fast_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.auto_full)
        )
        layout.addWidget(fast_mode, 2, 2)
