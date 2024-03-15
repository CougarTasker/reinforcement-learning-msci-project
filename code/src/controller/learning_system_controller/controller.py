from multiprocessing import Process
from typing import Optional

from typing_extensions import Self

from src.model.learning_system.learning_system import LearningSystem

from .state_update_bridge import StateUpdateBridge
from .user_action_bridge import UserAction, UserActionBridge
from .user_action_handlers.responsibility_chain import (
    UserActionResponsibilityChain,
)


class LearningSystemController(object):
    """Controller for managing learning systems."""

    def __init__(self) -> None:
        """Initialise the learning system controller."""
        self.system = LearningSystem()

        self.user_action_bridge = UserActionBridge()
        self.state_update_bridge = StateUpdateBridge()

        self.model_process: Optional[Process] = None

    def __enter__(self) -> Self:
        """Enter the context manager.

        the context manager is used for cleaning up processes gracefully.

        Returns:
            Self: the factory.
        """
        self.model_process = Process(
            target=self.model_mainloop, name="model_mainloop", daemon=True
        )
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
        chain = UserActionResponsibilityChain(self.system)
        while True:
            message = user_action_bridge.get_action_non_blocking()

            if message is None:
                if chain.handle_inaction():
                    self.send_current_state()
            else:
                if message.action is UserAction.end:
                    break
                chain.handle_user_action(message)
                self.send_current_state()

    def send_current_state(self):
        """Send the current state to the view."""
        current_state = self.system.get_current_state()
        self.state_update_bridge.update_state(current_state)
