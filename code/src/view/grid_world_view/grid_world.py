from enum import Enum
from tkinter import Widget
from typing import Any, Dict

from customtkinter import CTkButton, CTkFrame, CTkOptionMenu, CTkSegmentedButton

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction

from ...model.learning_system.cell_configuration import DisplayMode
from .display_state.display import DisplayState


class AutoSpeed(Enum):
    """Enumerates all possible auto speeds."""

    manual = 0  # one step at a time
    auto_local = 1  # step as fast as the states can be rendered
    auto_full = 2  # full speed just show what states we can


class GridWorld(CTkFrame):
    """Show the grid world and allow the user to step through it."""

    def __init__(self, master: Any, system: LearningSystemController):
        """Initialise the grid world view.

        given a system this widget will show the grid world and allow the
        user to step through it.

        Args:
            master (Any): the widget to draw this view into
            system (LearningSystemController): the controller to send actions
            to.
        """
        super().__init__(master)

        self.action_bridge = system.user_action_bridge
        self.update_bridge = system.state_update_bridge
        self.auto_mode = AutoSpeed.manual

        columns = (0, 1, 2, 3)
        self.grid_columnconfigure(columns, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._display = DisplayState(self)
        self._display.grid(
            row=1, column=0, columnspan=len(columns), sticky="nsew"
        )

        self.__setup_controls()

        # setup initial state
        self.__start_update_loop()
        self.action_bridge.submit_action(UserAction.fetch_current_state)

    def next_button_pressed(self):
        """When the next button is presses step the state forward."""
        self.action_bridge.submit_action(UserAction.one_step)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.action_bridge.submit_action(UserAction.reset)

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
        display_mode = self.display_mode_options[option]
        self.action_bridge.submit_action(
            UserAction.set_display_mode, display_mode
        )

    auto_mode_options = {
        "manual": AutoSpeed.manual,
        "auto": AutoSpeed.auto_local,
        "fast": AutoSpeed.auto_full,
    }

    def toggle_auto(self, key: str):
        """When the auto button has been pressed.

        automatically press the next button

        Args:
            key (str): the mode selected.
        """
        last_mode = self.auto_mode
        self.auto_mode = self.auto_mode_options[key]
        if last_mode is self.auto_mode:
            return
        self._next_button.configure(
            state="normal" if self.auto_mode is AutoSpeed.manual else "disabled"
        )

        if self.auto_mode is AutoSpeed.auto_full:
            self.action_bridge.submit_action(UserAction.start_auto)
        elif last_mode is AutoSpeed.auto_full:
            self.action_bridge.submit_action(UserAction.stop_auto)

    def __setup_controls(self):
        self._display_mode = CTkOptionMenu(
            self,
            values=list(self.display_mode_options.keys()),
            command=self.display_mode_changed,
        )
        default_display_mode = self.__invert_dict_search(
            self.display_mode_options, DisplayMode.default
        )
        self._display_mode.set(default_display_mode)
        self.__place_control(self._display_mode, 0)

        self._reset_button = CTkButton(
            self, text="reset", command=self.reset_button_pressed
        )
        self.__place_control(self._reset_button, 1)

        self._auto_progress = CTkSegmentedButton(
            self,
            values=list(self.auto_mode_options.keys()),
            command=self.toggle_auto,
        )
        default_auto_mode = self.__invert_dict_search(
            self.auto_mode_options, self.auto_mode
        )
        self._auto_progress.set(default_auto_mode)
        self.__place_control(self._auto_progress, 2)

        self._next_button = CTkButton(
            self, text="next", command=self.next_button_pressed
        )
        self.__place_control(self._next_button, 3)

    def __place_control(self, control: Widget, column: int):
        control.grid(row=2, column=column, pady=10)

    def __invert_dict_search(self, dictionary: Dict, default: Any) -> Any:
        return {enum_value: key for key, enum_value in dictionary.items()}[
            default
        ]

    def __start_update_loop(self):
        self.after_idle(self.__update_loop)

    def __update_loop(self):
        # when not busy update the state if available
        state = self.update_bridge.get_latest_state()
        if state is not None:
            self._display.set_state(state)
        if self.auto_mode is AutoSpeed.auto_local:
            # ready for next state
            self.next_button_pressed()
        self.update()
        self.after(100, self.__update_loop)
