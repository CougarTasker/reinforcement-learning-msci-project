from src.controller.user_action_bridge import UserAction, UserActionMessage
from src.controller.user_action_handlers.base_handler import (
    BaseUserActionHandler,
    HandleResult,
)
from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.learning_system.options import AgentOptions


class SetOptionsHandler(BaseUserActionHandler):
    """Handles requests to set the options."""

    default_strategies = {
        AgentOptions.q_learning: ExplorationStrategyOptions.epsilon_greedy,
        AgentOptions.value_iteration: ExplorationStrategyOptions.not_applicable,
        AgentOptions.value_iteration_optimised: (
            ExplorationStrategyOptions.not_applicable
        ),
    }

    def handle_action(self, user_action: UserActionMessage) -> HandleResult:
        """Handle the actions that change the options.

        Args:
            user_action (UserActionMessage): the user action provided

        Returns:
            HandleResult: weather this handler has been able to deal with the
                request.
        """
        match user_action:
            case UserActionMessage(
                action=UserAction.set_display_mode, payload=display_mode
            ):
                self.set_options(display_mode=display_mode)

            case UserActionMessage(action=UserAction.set_agent, payload=agent):
                self.set_top_level_options(
                    agent=agent,
                    exploration_strategy=self.default_strategies[agent],
                )

            case UserActionMessage(
                action=UserAction.set_dynamics, payload=dynamics
            ):
                self.set_top_level_options(dynamics=dynamics)

            case UserActionMessage(
                action=UserAction.set_agent_strategy, payload=agent_strategy
            ):
                self.set_top_level_options(exploration_strategy=agent_strategy)

            case _:
                return HandleResult.fail

        return HandleResult.success
