from src.model.learning_system.learning_system import LearningSystem
from src.model.learning_system.options import AgentOptions, DynamicsOptions

from ..view.App import ReinforcementLearningApp


class Controller(object):
    """Main controller class for managing updating the model."""

    def __init__(self) -> None:
        """Initialise the controller."""
        self.app = ReinforcementLearningApp()

    def start(self):
        """Start the application."""
        self.app.mainloop()

    def get_learning_system(
        self, agent: AgentOptions, dynamics: DynamicsOptions
    ) -> LearningSystem:
        """Get a particular learning system.

        Args:
            agent (AgentOptions): the agent in the system
            dynamics (DynamicsOptions): the dynamics to use in the system

        Returns:
            LearningSystem: the learning instance the represents this pair
        """
        return LearningSystem(agent, dynamics)
