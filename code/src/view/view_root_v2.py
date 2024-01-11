from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTabWidget, QWidget
from qdarktheme import setup_theme

from src.controller.learning_system_controller_factory import (
    LearningSystemControllerFactory,
)
from src.model.config.reader import ConfigReader
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.grid_world_view_v2.grid_world_v2 import GridWorld


class ReinforcementLearningApp(QWidget):
    """This is the root of the applications main UI."""

    tab_labels = {
        AgentOptions.value_iteration_optimised: "Value Iteration",
        AgentOptions.q_learning: "Q-Learning",
    }

    def __init__(
        self, controller_factory: LearningSystemControllerFactory
    ) -> None:
        """Instantiate the applications user interface.

        Args:
            controller_factory (LearningSystemControllerFactory): the controller
            responsible for managing user actions.
        """
        super().__init__(parent=None, f=Qt.WindowType.Window)
        self.setWindowTitle("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        tabs = QTabWidget(self)
        for agent, label in self.tab_labels.items():
            controller = controller_factory.create_controller(
                agent, DynamicsOptions.collection
            )
            grid_world = GridWorld(None, controller)
            tabs.addTab(grid_world, label)
        layout = QGridLayout(self)
        layout.addWidget(tabs)

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        setup_theme(config.appearance_mode())
        width, height = config.initial_size().split("x")
        self.resize(int(width), int(height))
