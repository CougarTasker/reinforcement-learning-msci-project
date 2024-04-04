from src.controller.state_update_bridge import StateUpdateBridge
from src.controller.user_action_bridge import (
    UserAction,
    UserActionBridge,
    UserActionMessage,
)
from src.model.learning_system.learning_system import LearningSystem


class LearningSystemController(object):
    """Controller for managing learning systems."""

    def __init__(
        self,
        system: LearningSystem,
    ) -> None:
        """Initialise the learning system controller.

        Args:
            system (LearningSystem): the learning system to control
        """
        self.system = system

        self.user_action_bridge = UserActionBridge()
        self.state_update_bridge = StateUpdateBridge()
        self.auto = False

    def model_mainloop(
        self,
    ):
        """Run the main loop of the model process.

        Raises:
            RuntimeError: if an unsupported action is made.
        """
        user_action_bridge = self.user_action_bridge
        while True:
            action = None
            if self.auto:
                while action is None:
                    action = user_action_bridge.get_action_non_blocking()
                    self.one_step()
            else:
                action = user_action_bridge.get_action()

            match action:
                case UserActionMessage(action=UserAction.end):
                    break
                case UserActionMessage(action=UserAction.one_step):
                    self.one_step()
                    self.send_current_state()
                case UserActionMessage(action=UserAction.start_auto):
                    self.auto = True
                case UserActionMessage(action=UserAction.stop_auto):
                    self.auto = False
                case UserActionMessage(action=UserAction.reset):
                    self.system.reset_state()
                    self.send_current_state()
                case UserActionMessage(action=UserAction.fetch_current_state):
                    self.send_current_state()
                case UserActionMessage(
                    action=UserAction.set_display_mode, payload=display_mode
                ):
                    self.system.set_display_mode(display_mode)
                    self.send_current_state()
                case _:
                    raise RuntimeError("Unknown action performed.")

    def one_step(self):
        """Perform one step."""
        self.system.perform_action()
        self.send_current_state()

    def send_current_state(self):
        """Send the current state to the view."""
        current_state = self.system.get_current_state()
        self.state_update_bridge.update_state(current_state)