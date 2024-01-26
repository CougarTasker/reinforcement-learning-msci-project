from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget
from qdarktheme import setup_theme

from src.controller.learning_system_controller import LearningSystemController
from src.model.config.reader import ConfigReader
from src.model.learning_system.options import AgentOptions
from src.view.controls.control_factory import ControlFactory
from src.view.grid_world_view_v2.grid_world_v2 import GridWorld
from src.view.option_controls import OptionControls
from src.view.state_publisher import StatePublisher


class ReinforcementLearningApp(QWidget):
    """This is the root of the applications main UI."""

    tab_labels = {
        AgentOptions.value_iteration_optimised: "Value Iteration",
        AgentOptions.q_learning: "Q-Learning",
    }

    def __init__(self, controller: LearningSystemController) -> None:
        """Instantiate the applications user interface.

        Args:
            controller (LearningSystemController): the controller
            responsible for managing user actions.
        """
        super().__init__(parent=None, f=Qt.WindowType.Window)
        self.setWindowTitle("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        self.publisher = StatePublisher(self, controller)
        layout = QGridLayout(self)

        control_factory = ControlFactory(controller, self.publisher)

        self.controls = OptionControls(self, control_factory)
        layout.addWidget(self.controls, 0, 0)

        self.grid_world = GridWorld(self, controller)
        layout.addWidget(self.grid_world, 1, 0)
        self.publisher.subscribe(self.grid_world)

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        setup_theme(config.appearance_mode())
        width, height = config.initial_size().split("x")
        self.resize(int(width), int(height))
