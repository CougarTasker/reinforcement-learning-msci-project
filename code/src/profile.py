# flake8: noqa

import cProfile
import pstats
from random import seed

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.controller.learning_system_controller.controller import (
    LearningSystemController,
)
from src.controller.learning_system_controller.user_action_bridge import (
    UserAction,
)
from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.hyperparameters.parameter_evaluator import ParameterEvaluator
from src.model.hyperparameters.random_search.random_parameter_strategy import (
    RandomParameterStrategy,
)
from src.model.hyperparameters.random_search.random_search import RandomSearch
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.global_options import (
    AutomaticOptions,
    GlobalOptions,
)
from src.model.learning_system.top_level_entities.options import (
    AgentOptions,
    DynamicsOptions,
    TopEntitiesOptions,
)
from src.view.display_state_v2.display import DisplayState
from src.view.view_root_v2 import ReinforcementLearningApp

from .model.learning_system.learning_system import LearningSystem

application_size = 1000


def one_process_profiling():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    ls = LearningSystem()
    top_level_options = TopEntitiesOptions(
        AgentOptions.value_iteration_optimised,
        DynamicsOptions.collection,
        ExplorationStrategyOptions.not_applicable,
    )
    ls.update_options(
        GlobalOptions(
            top_level_options,
            DisplayMode.state_value,
            AutomaticOptions.automatic_playing,
        )
    )

    qt = QApplication()
    display_state = DisplayState(None)
    display_state.show()
    display_state.resize(application_size, application_size)

    def loop():
        cs = ls.get_current_state()
        display_state.visible_state_updated(cs)
        ls.learning_instance.perform_action()

    timer = QTimer(display_state)
    timer.timeout.connect(loop)
    timer.start(1)
    qt.exec()


def end_to_end_profiling():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    with LearningSystemController() as main_controller:
        with HyperParameterController() as report_controller:
            main_controller.user_action_bridge.submit_action(
                UserAction.select_auto, AutomaticOptions.automatic_playing
            )
            qt = QApplication()
            app = ReinforcementLearningApp(main_controller, report_controller)
            app.show()
            qt.exec()


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    rs = RandomSearch()
    rs.running.set(True)
    seed(10)
    for i in range(5):
        print(i)
        for options in rs.search_options:
            if not rs.running.get():
                return
            hyper_parameters = RandomParameterStrategy()

            total_reward = ParameterEvaluator.evaluate_reward(
                options, hyper_parameters, rs.running
            )

            if not rs.running.get():
                return

            with rs.state_lock:
                state = rs.state.get()
                rs.state.set(
                    state.record_result(options, hyper_parameters, total_reward)
                )


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
