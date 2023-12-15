from PySide6.QtWidgets import QComboBox, QGridLayout, QPushButton, QWidget

from src.controller.state_update_bridge import StateUpdateBridge
from src.controller.user_action_bridge import UserAction, UserActionBridge
from src.model.learning_system.cell_configuration import DisplayMode


class Controls(QWidget):
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
        super().__init__(parent)

        self.action_bridge = action_bridge

        layout = QGridLayout(self)

        self.display_mode = QComboBox()
        self.display_mode.addItems(list(self.display_mode_options.keys()))
        self.display_mode.currentTextChanged.connect(self.display_mode_changed)
        layout.addWidget(self.display_mode, 0, 0)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_button_pressed)
        layout.addWidget(self.reset_button, 0, 1)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_button_pressed)
        layout.addWidget(self.next_button, 0, 2)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.action_bridge.submit_action(UserAction.reset)

    def next_button_pressed(self):
        """When the next button is presses step the state forward."""
        self.action_bridge.submit_action(UserAction.one_step)

    def display_mode_changed(self, option: str):
        """When the display mode option menu is selected.

        Args:
            option (str): the mode selected
        """
        display_mode = self.display_mode_options[option]
        self.action_bridge.submit_action(
            UserAction.set_display_mode, display_mode
        )
