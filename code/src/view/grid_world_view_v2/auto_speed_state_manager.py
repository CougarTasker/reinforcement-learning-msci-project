from enum import Enum

from PySide6.QtCore import QTimer

from src.controller.user_action_bridge import UserAction, UserActionBridge


class AutoSpeed(Enum):
    """Enumerates all possible auto speeds."""

    manual = 0  # one step at a time
    auto_local = 1  # step as fast as the states can be rendered
    auto_full = 2  # full speed just show what states we can


class ProgressButtonMode(Enum):
    """Enumerates all the different modes of the progress button."""

    manual = 0
    pause = 1
    restart = 2


class AutoStateManager(object):
    """Manages the state for the auto progress feature."""

    auto_speed_ms = 300

    progress_button_text = {
        ProgressButtonMode.manual: "Next",
        ProgressButtonMode.pause: "Pause",
        ProgressButtonMode.restart: "Start",
    }

    def __init__(self, action_bridge: UserActionBridge) -> None:
        """Initialise the state manager.

        initially in the manual mode

        Args:
            action_bridge (UserActionBridge): update the controller with the
            user's action.
        """
        self.current_speed = AutoSpeed.manual
        self.paused = False
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.__one_step)
        self.action_bridge = action_bridge

    def set_speed(self, speed: AutoSpeed):
        """Set the current speed.

        Args:
            speed (AutoSpeed): the new speed (mode) to operate in.
        """
        if speed is self.current_speed:
            return

        self.__stop_mode(self.current_speed)

        self.paused = False

        self.__start_mode(speed)
        self.current_speed = speed

    def progress_button_pressed(self):
        """Handle the progress button being pressed.

        the action performed by this depends on the mode of the button.

        """
        match self.__progress_button_mode():
            case ProgressButtonMode.manual:
                self.__one_step()
            case ProgressButtonMode.pause:
                self.__stop_mode(self.current_speed)
                self.paused = True
            case ProgressButtonMode.restart:
                self.__start_mode(self.current_speed)
                self.paused = False

    def get_progress_button_text(self) -> str:
        """Get the label for the progress button.

        This indicates to the user what this button will perform.

        Returns:
            str: the current label for the button.
        """
        return self.progress_button_text[self.__progress_button_mode()]

    def __progress_button_mode(self) -> ProgressButtonMode:
        if self.current_speed is AutoSpeed.manual:
            return ProgressButtonMode.manual

        if self.paused:
            return ProgressButtonMode.restart

        return ProgressButtonMode.pause

    def __one_step(self):
        self.action_bridge.submit_action(UserAction.one_step)

    def __stop_mode(self, mode: AutoSpeed):
        match mode:
            case AutoSpeed.auto_local:
                self.auto_timer.stop()
            case AutoSpeed.auto_full:
                self.action_bridge.submit_action(UserAction.stop_auto)

    def __start_mode(self, mode: AutoSpeed):
        match mode:
            case AutoSpeed.auto_local:
                self.auto_timer.start(self.auto_speed_ms)
            case AutoSpeed.auto_full:
                self.action_bridge.submit_action(UserAction.start_auto)
