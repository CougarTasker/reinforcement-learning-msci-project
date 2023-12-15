import cProfile
import pstats

from PySide6.QtCore import QTimer

# import customtkinter
from PySide6.QtWidgets import QApplication

from src.model.learning_system.cell_configuration import DisplayMode
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.grid_world_view_v2.display_state_v2.display import DisplayState

from .model.learning_system.learning_system import LearningSystem

# from src.view.grid_world_view.display_state.display import DisplayState


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    ls = LearningSystem(
        AgentOptions.value_iteration, DynamicsOptions.collection
    )

    ls.set_display_mode(DisplayMode.state_value)

    qt = QApplication()
    d = DisplayState(None)
    d.show()
    d.resize(500, 500)

    def loop():
        cs = ls.get_current_state()
        d.set_state(cs)
        ls.perform_action()

    timer = QTimer(d)
    timer.timeout.connect(loop)
    timer.start(1)
    qt.exec()


# def profiled_code_tkinter():
#     """Run the profiled code.

#     The code in this method will be profiled by the application.
#     """
#     ls = LearningSystem(
#         AgentOptions.value_iteration, DynamicsOptions.collection
#     )

#     ls.set_display_mode(DisplayMode.state_value)

#     app = customtkinter.CTk()
#     app.geometry("1500x800")
#     d = DisplayState(app)
#     app.grid_columnconfigure(0, weight=1)
#     app.grid_rowconfigure(0, weight=1)
#     d.grid(row=0, column=0, sticky="nesw")

#     def loop(i=0):
#         if i > 50:
#             app.destroy()
#             return

#         cs = ls.get_current_state()
#         d.set_state(cs)
#         ls.perform_action()
#         app.after(100, loop, i + 1)

#     app.after(100, loop)
#     app.mainloop()


def profile():
    """Entry point for profiling the application."""
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        profiled_code()
    except BaseException:
        pass
    finally:
        profiler.disable()
        ps = pstats.Stats(profiler)
        ps.dump_stats("profile_result.prof")


if __name__ == "__main__":
    profile()
