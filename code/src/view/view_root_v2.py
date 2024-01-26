from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget
from qdarktheme import setup_theme

from src.controller.learning_system_controller import LearningSystemController
from src.model.config.reader import ConfigReader
from src.model.learning_system.options import AgentOptions
from src.view.controls.control_factory import ControlFactory
from src.view.display_state_v2.display import DisplayState
from src.view.interaction_controls import InteractionControls
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

        self.option_controls = OptionControls(self, control_factory)
        layout.addWidget(self.option_controls, 0, 0)

        self.display_state = DisplayState(self)
        layout.addWidget(self.display_state, 1, 0)
        self.publisher.subscribe(self.display_state)
        layout.setRowStretch(1, 1)

        self.interaction_controls = InteractionControls(self, control_factory)
        layout.addWidget(self.interaction_controls, 2, 0)

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        setup_theme(config.appearance_mode())
        width, height = config.initial_size().split("x")
        self.resize(int(width), int(height))
