from customtkinter import (
    CTk,
    CTkLabel,
    set_appearance_mode,
    set_default_color_theme,
)

from src.model.config.reader import ConfigReader

from ..controller.learning_instance_controller import InstanceController
from ..controller.options import AgentOptions, DynamicsOptions
from .grid_world_view.view import GridPadding


class ReinforcementLearningApp(CTk):
    """Root of the application's view."""

    def __init__(self):
        """Initialise the custom tkinter app."""
        super().__init__()
        self.title("RHUL MSci FYP - Reinforcement Learning App")
        self.setup_config()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1, minsize=0)

        CTkLabel(self, text="Reinforcement Learning App").grid(row=0, column=0)

        self.controller = InstanceController(
            AgentOptions.value_iteration, DynamicsOptions.collection
        )
        GridPadding(self, self.controller.get_current_state()).grid(
            row=1, column=0, columnspan=2, sticky="nsew"
        )

    def setup_config(self):
        """Set app properties from config."""
        config = ConfigReader().gui()
        set_appearance_mode(config.appearance_mode())
        set_default_color_theme(config.color_theme())
