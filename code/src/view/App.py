from customtkinter import (
    CTk,
    CTkLabel,
    CTkTabview,
    set_appearance_mode,
    set_default_color_theme,
)

from src.model.config.reader import ConfigReader
from src.model.learning_system.learning_system import LearningSystem

from ..model.learning_system.options import AgentOptions, DynamicsOptions
from .grid_world_view.grid_world import GridWorld


class ReinforcementLearningApp(CTk):
    """Root of the application's view."""

    tab_definitions = {
        "Value Iteration": AgentOptions.value_iteration_optimised,
        "Q Learning": AgentOptions.q_learning,
    }

    def __init__(self):
        """Initialise the custom tkinter app."""
        super().__init__()
        self.title("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1, minsize=0)

        CTkLabel(self, text="Reinforcement Learning App").grid(row=0, column=0)

        self.tabs = CTkTabview(self)
        self.tabs.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.__populate_tabs()

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        set_appearance_mode(config.appearance_mode())
        set_default_color_theme(config.color_theme())
        self.geometry(config.initial_size())

    def __populate_tabs(self):
        """Create the tabs for each agent."""
        for tab_name, agent in self.tab_definitions.items():
            tab_frame = self.tabs.add(tab_name)
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(0, weight=1)
            GridWorld(
                tab_frame,
                LearningSystem(agent, DynamicsOptions.collection),
            ).grid(row=0, column=0, sticky="nsew")
