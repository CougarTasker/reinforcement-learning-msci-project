from typing import Any

from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkOptionMenu

from src.controller.cell_configuration import DisplayMode

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

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.cumulative_reward: float = 0
        self._reward_label = CTkLabel(self)
        self._reward_label.grid(row=0, column=0)
        self.set_reward_text()

        self._display = DisplayState(self, self.controller.get_current_state())
        self._display.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.__setup_controls()

    def set_reward_text(self):
        """Update the reward text."""
        self._reward_label.configure(
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
        self._display.set_state(current_state)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.cumulative_reward = 0
        self.set_reward_text()
        new_state = self.controller.reset_state()
        self._display.set_state(new_state)

    display_mode_options = {
        "default": DisplayMode.default,
        "best action": DisplayMode.best_action,
        "state value": DisplayMode.state_value,
        "action value": DisplayMode.action_value_global,
        "action value local": DisplayMode.action_value_local,
    }

    def display_mode_changed(self, option: str):
        """When the display mode option menu is selected.

        Args:
            option (str): the mode selected
        """
        self.controller.set_display_mode(self.display_mode_options[option])
        self._display.set_state(self.controller.get_current_state())

    def __setup_controls(self):
        self._reset_button = CTkButton(
            self, text="reset", command=self.reset_button_pressed
        )
        self._reset_button.grid(row=2, column=1)

        self._next_button = CTkButton(
            self, text="next", command=self.next_button_pressed
        )
        self._next_button.grid(row=2, column=2)

        self._display_mode = CTkOptionMenu(
            self,
            values=list(self.display_mode_options.keys()),
            command=self.display_mode_changed,
        )
        self._display_mode.grid(row=2, column=0)
