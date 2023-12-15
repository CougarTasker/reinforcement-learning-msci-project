from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QGridLayout, QWidget

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.view.grid_world_view_v2.controls import Controls
from src.view.grid_world_view_v2.display_state_v2.display import DisplayState


class GridWorld(QWidget):
    def __init__(
        self, parent: QWidget, system: LearningSystemController
    ) -> None:
        super().__init__(parent)

        self.update_bridge = system.state_update_bridge
        self.action_bridge = system.user_action_bridge

        self.display = DisplayState(self)
        layout = QGridLayout(self)

        layout.addWidget(self.display, 0, 0)

        self.controls = Controls(self, self.action_bridge)
        layout.addWidget(self.controls, 1, 0)

        timer = QTimer(self)
        timer.timeout.connect(self.check_for_work)
        timer.start(100)

        self.action_bridge.submit_action(UserAction.fetch_current_state)

    def check_for_work(self):
        state = self.update_bridge.get_latest_state()
        if state is not None:
            self.display.set_state(state)
