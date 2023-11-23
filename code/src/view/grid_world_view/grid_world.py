from typing import Any

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ...controller.learning_instance_controller import InstanceController
from .display_state.display import DisplayState


class GridWorld(CTkFrame):
    """Show the grid world and allow the user to step through it."""

    def __init__(self, master: Any, controller: InstanceController):
        """Initialise the grid world view.

        given a controller this widget will show the grid world and allow the
        user to step through it.

        Args:
            master (Any): the widget to draw this view into
            controller (InstanceController): the controller to send actions to.
        """
        super().__init__(master)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        self.cumulative_reward: float = 0
        self.reward_label = CTkLabel(self)
        self.reward_label.grid(row=0, column=0)
        self.set_reward_text()

        self.grid_rowconfigure(1, weight=1)
        self.display = DisplayState(self, self.controller.get_current_state())
        self.display.grid(row=1, column=0, sticky="nsew")
        self.next_button = CTkButton(
            self, text="next", command=self.next_button_pressed
        )
        self.next_button.grid(row=2, column=0)

    def set_reward_text(self):
        """Update the reward text."""
        self.reward_label.configure(
            text=f"cumulative reward: {self.cumulative_reward}"
        )

    def next_button_pressed(self):
        """When the next button is presses step the state forward."""
        (
            _previous_state,
            _action,
            current_state,
            reward,
        ) = self.controller.perform_action()
        self.cumulative_reward += reward
        self.set_reward_text()
        self.display.set_state(current_state)
