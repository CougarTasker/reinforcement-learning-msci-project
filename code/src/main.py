import sys

from PySide6.QtWidgets import QApplication

from .controller.learning_system_controller import LearningSystemController
from .view.view_root_v2 import ReinforcementLearningApp


def main():
    """Start the application.

    The main entry point into the application.
    """
    with LearningSystemController() as controller:
        qt = QApplication(sys.argv)
        app = ReinforcementLearningApp(controller)
        app.show()
        qt.exec()


if __name__ == "__main__":
    main()
