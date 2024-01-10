import cProfile
import pstats

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.model.learning_system.cell_configuration import DisplayMode
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.grid_world_view_v2.display_state_v2.display import DisplayState

from .model.learning_system.learning_system import LearningSystem

application_size = 500


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    ls = LearningSystem(
        AgentOptions.value_iteration, DynamicsOptions.collection
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
