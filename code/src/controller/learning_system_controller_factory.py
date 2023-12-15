from multiprocessing import Process
from typing import List

from src.controller.learning_system_controller import LearningSystemController
from src.controller.user_action_bridge import UserAction
from src.model.learning_system.learning_system import LearningSystem
from src.model.learning_system.options import AgentOptions, DynamicsOptions


class LearningSystemControllerFactory(object):
    """Factory method for creating LearningSystemControllers."""

    def __init__(self) -> None:
        self.processes: List[Process] = []
        self.controllers: List[LearningSystemController] = []

    def create_controller(
        self, agent: AgentOptions, dynamics: DynamicsOptions
    ) -> LearningSystemController:
        """Create a new LearningSystemController.

        Args:
            agent (AgentOptions): the agent in the learning system.
            dynamics (DynamicsOptions): the dynamics in the learning system.

        Returns:
            LearningSystemController: The controller
        """
        system = LearningSystem(agent, dynamics)
        controller = LearningSystemController(system)

        model_process = Process(target=controller.model_mainloop, daemon=True)
        model_process.start()
        self.processes.append(model_process)
        self.controllers.append(controller)
        return controller

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        for controller in self.controllers:
            controller.user_action_bridge.submit_action(UserAction.end)

        for process in self.processes:
            process.join()
