from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTabWidget, QWidget
from qdarktheme import setup_theme

from src.controller.learning_system_controller.controller import (
    LearningSystemController,
)
from src.controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from src.model.config.reader import ConfigReader
from src.view.controls.control_factory import ControlFactory
from src.view.display_state_v2.display import DisplayState
from src.view.interaction_controls import InteractionControls
from src.view.option_controls import OptionControls
from src.view.state_publisher import StatePublisher
from src.view.statistics.reward_history import RewardHistory


class ReinforcementLearningApp(QWidget):
    """This is the root of the applications main UI."""

    def __init__(
        self,
        main_controller: LearningSystemController,
        report_controller: ReportGeneratorController,
    ) -> None:
        """Instantiate the applications user interface.

        Args:
            main_controller (LearningSystemController): the controller
                responsible for managing the main learning system.
            report_controller (ReportGeneratorController): the controller
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

        self.main_tab_area = self.__create_tab_widget()
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

    def __create_tab_widget(self):
        main_tab_area = QTabWidget(self)

        display_state = DisplayState(None)
        self.publisher.subscribe(display_state)
        main_tab_area.addTab(display_state, "Current State")

        reward_history = RewardHistory(None)
        self.publisher.subscribe(reward_history)
        main_tab_area.addTab(reward_history, "Reward History")

        return main_tab_area
