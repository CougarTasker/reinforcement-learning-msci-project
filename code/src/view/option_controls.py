from PySide6.QtWidgets import QGridLayout, QGroupBox, QWidget

from src.controller.user_action_bridge import UserAction
from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.model.learning_system.top_level_entities.options import (
    AgentOptions,
    DynamicsOptions,
)
from src.view.controls.control_factory import ControlFactory
from src.view.controls.custom_combo_widget import ComboWidgetState


class OptionControls(QGroupBox):
    """Widget that contains the controls for interacting with the grid world."""

    agent_options = {
        "Value Iteration": AgentOptions.value_iteration_optimised,
        "Q-Learning": AgentOptions.q_learning,
    }

    not_applicable = ComboWidgetState(
        {"Not Applicable": ExplorationStrategyOptions.not_applicable},
        "Not Applicable",
        enabled=False,
    )

    exploration_strategy_options = {
        "Epsilon Greedy": ExplorationStrategyOptions.epsilon_greedy,
        "Upper Confidence Bound": (
            ExplorationStrategyOptions.upper_confidence_bound
        ),
    }

    dynamics_options = {
        "Collection": DynamicsOptions.collection,
        "Cliff": DynamicsOptions.cliff,
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

        agent_strategy = control_factory.create_combo_state(
            self,
            self.not_applicable,
            UserAction.set_agent_strategy,
            self.__strategy_combo_responsive_options,
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

    def __strategy_combo_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        strategy = state.global_options.top_level_options.exploration_strategy
        if strategy is ExplorationStrategyOptions.not_applicable:
            return self.not_applicable

        reverse_options = {
            option: label
            for label, option in self.exploration_strategy_options.items()
        }

        selected = reverse_options[strategy]

        return ComboWidgetState(self.exploration_strategy_options, selected)
