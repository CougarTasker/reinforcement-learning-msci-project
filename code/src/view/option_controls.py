from PySide6.QtWidgets import QGridLayout, QGroupBox, QWidget

from src.controller.user_action_bridge import UserAction
from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.learning_system.options import AgentOptions, DynamicsOptions
from src.view.controls.control_factory import ControlFactory


class OptionControls(QGroupBox):
    """Widget that contains the controls for interacting with the grid world."""

    agent_options = {
        "Value Iteration": AgentOptions.value_iteration_optimised,
        "Q-Learning": AgentOptions.q_learning,
    }

    agent_strategy_options = {
        "Epsilon-greedy": ExplorationStrategyOptions.epsilon_greedy
    }

    dynamics_options = {
        "Collection": DynamicsOptions.collection,
    }

    group_title = "Simulation Configuration Controls"

    reset_button_text = "reset"

    def __init__(
        self, parent: QWidget, control_factory: ControlFactory
    ) -> None:
        """Initialise the option controls.

        Args:
            parent (QWidget): the parent of this widget.
            control_factory (ControlFactory): the factory to make the controls
                with.
        """
        super().__init__(self.group_title, parent)

        layout = QGridLayout(self)

        agent = control_factory.create_combo(
            self, self.agent_options, UserAction.set_agent
        )
        layout.addWidget(agent, 0, 0)

        agent_strategy = control_factory.create_combo(
            self, self.agent_strategy_options, UserAction.set_agent_strategy
        )
        layout.addWidget(agent_strategy, 0, 1)

        dynamics = control_factory.create_combo(
            self, self.dynamics_options, UserAction.set_dynamics
        )
        layout.addWidget(dynamics, 0, 2)

        reset = control_factory.create_button(
            self, self.reset_button_text, UserAction.reset_system
        )
        layout.addWidget(reset, 0, 3)
