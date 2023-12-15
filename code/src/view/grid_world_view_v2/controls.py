from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget

from src.controller.state_update_bridge import StateUpdateBridge
from src.controller.user_action_bridge import UserAction, UserActionBridge


class Controls(QWidget):
    def __init__(
        self, parent: QWidget, action_bridge: UserActionBridge
    ) -> None:
        super().__init__(parent)

        self.action_bridge = action_bridge

        layout = QGridLayout(self)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_button_pressed)
        layout.addWidget(self.next_button, 0, 0)

    def next_button_pressed(self):
        self.action_bridge.submit_action(UserAction.one_step)
