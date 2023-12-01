from .controller.learning_system_controller_factory import (
    LearningSystemControllerFactory,
)
from .view.App import ReinforcementLearningApp


def main():
    """Start the application.

    The main entry point into the application.
    """
    controller = LearningSystemControllerFactory()
    app = ReinforcementLearningApp(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
