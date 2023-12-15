from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from src.controller.learning_system_controller_factory import (
    LearningSystemControllerFactory,
)
from src.model.config.reader import ConfigReader
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.grid_world_view_v2.grid_world_v2 import GridWorld


class ReinforcementLearningApp(QWidget):
    def __init__(self, controller: LearningSystemControllerFactory) -> None:
        super().__init__(parent=None, f=Qt.WindowType.Window)
        self.controller = controller
        self.setWindowTitle("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        self.grid_world = GridWorld(
            self,
            controller.create_controller(
                AgentOptions.value_iteration, DynamicsOptions.collection
            ),
        )

        layout = QGridLayout(self)
        layout.addWidget(self.grid_world)

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        # set_appearance_mode(config.appearance_mode())
        # set_default_color_theme(config.color_theme())
        width, height = config.initial_size().split("x")
        self.resize(int(width), int(height))
