from dataclasses import replace
from multiprocessing import Process

from git import Optional
from typing_extensions import Self

from src.controller.state_update_bridge import StateUpdateBridge
from src.controller.user_action_bridge import (
    UserAction,
    UserActionBridge,
    UserActionMessage,
)
from src.model.learning_system.learning_system import LearningSystem


class LearningSystemController(object):
    """Controller for managing learning systems."""

    def __init__(self) -> None:
        """Initialise the learning system controller."""
        self.system = LearningSystem()
        self.user_action_bridge = UserActionBridge()
        self.state_update_bridge = StateUpdateBridge()
        self.auto = False

        self.model_process: Optional[Process] = None

    def __enter__(self) -> Self:
        """Enter the context manager.

        the context manager is used for cleaning up processes gracefully.

        Returns:
            Self: the factory.
        """
        self.model_process = Process(target=self.model_mainloop, daemon=True)
        self.model_process.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """Exit the context, clean up the resources.

        Args:
            exc_type (Any): Not used.
            exc_value (Any): Not used.
            exc_tb (Any): Not used.
        """
        self.user_action_bridge.submit_action(UserAction.end)
        if self.model_process is not None:
            self.model_process.join()

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
                case UserActionMessage(action=UserAction.reset_state):
                    self.system.learning_instance.reset_state()
                    self.send_current_state()
                case UserActionMessage(action=UserAction.fetch_current_state):
                    self.send_current_state()
                case UserActionMessage(
                    action=UserAction.set_display_mode, payload=display_mode
                ):
                    self.system.update_options(
                        replace(self.system.options, display_mode=display_mode)
                    )
                    self.send_current_state()

                case UserActionMessage(
                    action=UserAction.set_agent, payload=agent
                ):
                    self.system.update_options(
                        replace(self.system.options, agent=agent)
                    )
                    self.send_current_state()
                case UserActionMessage(
                    action=UserAction.set_dynamics, payload=dynamics
                ):
                    self.system.update_options(
                        replace(self.system.options, dynamics=dynamics)
                    )
                    self.send_current_state()
                case UserActionMessage(
                    action=UserAction.set_agent_strategy, payload=agent_strategy
                ):
                    self.system.update_options(
                        replace(
                            self.system.options, agent_strategy=agent_strategy
                        )
                    )
                    self.send_current_state()
                case UserActionMessage(action=UserAction.reset_system):
                    self.system.reset_top_level()
                    self.send_current_state()
                case _:
                    raise RuntimeError("Unknown action performed.")

    def one_step(self):
        """Perform one step."""
        self.system.learning_instance.perform_action()
        self.send_current_state()

    def send_current_state(self):
        """Send the current state to the view."""
        current_state = self.system.get_current_state()
        self.state_update_bridge.update_state(current_state)
