from multiprocessing import Process

from src.controller.learning_system_controller import LearningSystemController
from src.model.learning_system.learning_system import LearningSystem
from src.model.learning_system.options import AgentOptions, DynamicsOptions


class LearningSystemControllerFactory(object):
    """Factory method for creating LearningSystemControllers."""

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

        return controller
