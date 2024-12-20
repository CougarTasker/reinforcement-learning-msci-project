from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget
from qdarktheme import setup_theme

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.controller.learning_system_controller.controller import (
    LearningSystemController,
)
from src.model.config.reader import ConfigReader
from src.view.controls.control_factory import ControlFactory
from src.view.interaction_controls import InteractionControls
from src.view.main_tab_area import MainTabArea
from src.view.option_controls import OptionControls
from src.view.state_publisher import StatePublisher


class ReinforcementLearningApp(QWidget):
    """This is the root of the applications main UI."""

    def __init__(
        self,
        main_controller: LearningSystemController,
        report_controller: HyperParameterController,
    ) -> None:
        """Instantiate the applications user interface.

        Args:
            main_controller (LearningSystemController): the controller
                responsible for managing the main learning system.
            report_controller (HyperParameterController): the controller
                responsible for creating reports.
        """
        super().__init__(parent=None, f=Qt.WindowType.Window)
        self.setWindowTitle("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        self.publisher = StatePublisher(self, main_controller)
        layout = QGridLayout(self)

        control_factory = ControlFactory(main_controller, self.publisher)

        self.option_controls = OptionControls(self, control_factory)
        layout.addWidget(self.option_controls, 0, 0)

        self.main_tab_area = MainTabArea(
            self, self.publisher, report_controller
        )
        layout.addWidget(self.main_tab_area, 1, 0)
        layout.setRowStretch(1, 1)

        self.interaction_controls = InteractionControls(self, control_factory)
        layout.addWidget(self.interaction_controls, 2, 0)

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui
        setup_theme(config.appearance_mode)
        width, height = config.initial_size
        self.resize(width, height)
