from enum import Enum

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QPushButton,
    QRadioButton,
    QWidget,
)

from src.controller.user_action_bridge import UserAction, UserActionBridge
from src.model.learning_system.cell_configuration import DisplayMode


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


class Controls(QWidget):
    """Widget that contains the controls for interacting with the grid world."""

    display_mode_options = {
        "default": DisplayMode.default,
        "best action": DisplayMode.best_action,
        "state value": DisplayMode.state_value,
        "action value": DisplayMode.action_value_global,
        "action value local": DisplayMode.action_value_local,
    }

    def __init__(
        self, parent: QWidget, action_bridge: UserActionBridge
    ) -> None:
        """Initialise the controls.

        Args:
            parent (QWidget): the parent of this widget.
            action_bridge (UserActionBridge): the channel to notify the
                controller of the users actions.
        """
        super().__init__(parent)

        self.action_bridge = action_bridge

        layout = QGridLayout(self)

        self.__add_display_mode(layout)

        self.__add_reset_button(layout)

        self.__add_auto_speed_toggles(layout)

        self.auto_mode_manger = AutoStateManager(action_bridge)

        self.progress_button = QPushButton(
            self.auto_mode_manger.get_progress_button_text()
        )
        self.progress_button.clicked.connect(self.progress_button_pressed)
        layout.addWidget(self.progress_button, 0, 3)

    def reset_button_pressed(self):
        """When the reset button is pressed. reset the state."""
        self.action_bridge.submit_action(UserAction.reset)

    def progress_button_pressed(self):
        """When the next button is presses step the state forward."""
        self.auto_mode_manger.progress_button_pressed()
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def auto_speed_toggled(self, speed: AutoSpeed):
        """Handle when new speed is selected.

        Args:
            speed (AutoSpeed): the new speed to operate.
        """
        self.auto_mode_manger.set_speed(speed)
        self.progress_button.setText(
            self.auto_mode_manger.get_progress_button_text()
        )

    def display_mode_changed(self, option: str):
        """When the display mode option menu is selected.

        Args:
            option (str): the mode selected
        """
        display_mode = self.display_mode_options[option]
        self.action_bridge.submit_action(
            UserAction.set_display_mode, display_mode
        )

    def __add_display_mode(self, layout: QGridLayout):
        display_mode = QComboBox()
        display_mode.addItems(list(self.display_mode_options.keys()))
        display_mode.currentTextChanged.connect(self.display_mode_changed)
        layout.addWidget(display_mode, 0, 0)

    def __add_reset_button(self, layout: QGridLayout):
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_button_pressed)
        layout.addWidget(reset_button, 0, 1)

    def __add_auto_speed_toggles(self, layout: QGridLayout):
        manual_mode = QRadioButton("Manual", self)
        manual_mode.setChecked(True)
        manual_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.manual)
        )
        layout.addWidget(manual_mode, 0, 2)

        auto_mode = QRadioButton("Auto", self)
        auto_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.auto_local)
        )
        layout.addWidget(auto_mode, 1, 2)

        fast_mode = QRadioButton("Fast", self)
        fast_mode.clicked.connect(
            lambda: self.auto_speed_toggled(AutoSpeed.auto_full)
        )
        layout.addWidget(fast_mode, 2, 2)
