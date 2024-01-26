import cProfile
import pstats

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.controller.learning_system_controller import LearningSystemController
from src.controller.learning_system_controller_factory import (
    LearningSystemControllerFactory,
)
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.cell_configuration import DisplayMode
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.grid_world_view_v2.display_state_v2.display import DisplayState
from src.view.view_root_v2 import ReinforcementLearningApp

from .model.learning_system.learning_system import LearningSystem

application_size = 1000


def one_process_profiling():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    ls = LearningSystem(
        AgentOptions.value_iteration_optimised, DynamicsOptions.collection
    )

    ls.set_display_mode(DisplayMode.state_value)

    qt = QApplication()
    display_state = DisplayState(None)
    display_state.show()
    display_state.resize(application_size, application_size)

    def loop():
        cs = ls.get_current_state()
        display_state.set_state(cs)
        ls.perform_action()

    timer = QTimer(display_state)
    timer.timeout.connect(loop)
    timer.start(1)
    qt.exec()


class ProfilingFactory(LearningSystemControllerFactory):
    """Controller factory, extended to automate the setting of the speed."""

    def create_controller(
        self, agent: AgentOptions, dynamics: DynamicsOptions
    ) -> LearningSystemController:
        """Create the controller.

        Args:
            agent (AgentOptions): _description_
            dynamics (DynamicsOptions): _description_

        Returns:
            LearningSystemController: _description_
        """
        ls = super().create_controller(agent, dynamics)
        if agent is AgentOptions.value_iteration_optimised:
            ls.user_action_bridge.submit_action(
                UserAction.set_display_mode, DisplayMode.state_value
            )
            ls.user_action_bridge.submit_action(UserAction.start_auto)

        return ls


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    with ProfilingFactory() as controller:
        qt = QApplication()
        app = ReinforcementLearningApp(controller)
        app.show()
        app.resize(application_size, application_size)
        qt.exec()


def profile():
    """Entry point for profiling the application."""
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        profiled_code()
    finally:
        profiler.disable()
        ps = pstats.Stats(profiler)
        ps.dump_stats("profile_result.prof")


if __name__ == "__main__":
    profile()
