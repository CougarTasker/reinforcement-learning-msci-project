from PySide6.QtWidgets import QGridLayout, QGroupBox, QWidget

from src.controller.learning_system_controller.user_action_bridge import (
    UserAction,
)
from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.learning_system.learning_system import LearningSystem
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.controls.control_factory import ControlFactory
from src.view.controls.custom_combo_widget import ComboWidgetState
from src.view.option_display_text import OptionDisplayText


class OptionControls(QGroupBox):
    """Widget that contains the controls for interacting with the grid world."""

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
            self,
            ComboWidgetState(
                OptionDisplayText.agent_options,
                LearningSystem.initial_top_options.agent,
            ),
            UserAction.set_agent,
            self.__agent_responsive_options,
        )
        layout.addWidget(agent, 0, 0)

        agent_strategy = control_factory.create_combo(
            self,
            ComboWidgetState(
                OptionDisplayText.not_applicable_exploration_option,
                LearningSystem.initial_top_options.exploration_strategy,
            ),
            UserAction.set_agent_strategy,
            self.__strategy_responsive_options,
        )
        layout.addWidget(agent_strategy, 0, 1)

        dynamics = control_factory.create_combo(
            self,
            ComboWidgetState(
                OptionDisplayText.dynamics_options,
                LearningSystem.initial_top_options.dynamics,
            ),
            UserAction.set_dynamics,
            self.__dynamics_responsive_options,
        )
        layout.addWidget(dynamics, 0, 2)

        reset = control_factory.create_button(
            self, self.reset_button_text, UserAction.reset_system
        )
        layout.addWidget(reset, 0, 3)

    def __strategy_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        strategy = state.global_options.top_level_options.exploration_strategy
        if strategy is ExplorationStrategyOptions.not_applicable:
            return ComboWidgetState(
                OptionDisplayText.not_applicable_exploration_option,
                ExplorationStrategyOptions.not_applicable,
                enabled=False,
            )

        return ComboWidgetState(
            OptionDisplayText.applicable_exploration_option, strategy
        )

    def __agent_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        return ComboWidgetState(
            OptionDisplayText.agent_options,
            state.global_options.top_level_options.agent,
        )

    def __dynamics_responsive_options(
        self, state: StateDescription
    ) -> ComboWidgetState:
        return ComboWidgetState(
            OptionDisplayText.dynamics_options,
            state.global_options.top_level_options.dynamics,
        )
