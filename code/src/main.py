import sys

from PySide6.QtWidgets import QApplication

from .controller.learning_system_controller.controller import (
    LearningSystemController,
)
from .controller.report_generation_controller.controller import (
    ReportGeneratorController,
)
from .view.view_root_v2 import ReinforcementLearningApp


def main():
    """Start the application.

    The main entry point into the application.
    """
    with LearningSystemController() as main_controller:
        with ReportGeneratorController() as report_controller:
            qt = QApplication(sys.argv)
            app = ReinforcementLearningApp(main_controller, report_controller)
            app.show()
            qt.exec()


if __name__ == "__main__":
    main()
