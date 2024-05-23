from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar

from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.global_options import AutomaticOptions
from src.model.learning_system.top_level_entities.options import (
    AgentOptions,
    DynamicsOptions,
)

Option = TypeVar("Option")


@dataclass(frozen=True, slots=True)
class DisplayTextListing(Generic[Option]):
    """Class for listing the display strings for each option."""

    texts: Dict[Option, str]

    def get_mapping(self) -> Dict[Option, str]:
        """Get the mapping from options to their display texts.

        Returns:
            Dict[Option, str]: mapping from options to their display text.
        """
        return self.texts

    def get_reverse_mapping(self) -> Dict[str, Option]:
        """Get the mapping from display text to the option.

        Returns:
            Dict[str, Option]: mapping from string to an option.
        """
        return {txt: opt for opt, txt in self.get_mapping().items()}

    def get_text(self, option: Option) -> str:
        """Get the display text for a given option.

        Args:
            option (Option): the option to lookup.

        Returns:
            str: the display text if the option is known.
        """
        return self.get_mapping()[option]

    def get_option(self, text: str) -> Option:
        """Get the option corresponding to the given display text.

        Args:
            text (str): the display text to lookup.

        Returns:
            Option: the option for this display text if one can be
                found.
        """
        return self.get_reverse_mapping()[text]

    def list_all_text(self) -> List[str]:
        """List all of the display text options.

        Returns:
            List[str]: list of all the display text options.
        """
        return list(self.get_mapping().values())

    def create_subset(self, *opts: Option) -> "DisplayTextListing[Option]":
        """Create a listing that is a subset of another.

        Args:
            opts (Option): The options to include in the subset.

        Returns:
            DisplayTextListing: the new display text listing with the reduced
                options.
        """
        return DisplayTextListing(
            {opt: txt for opt, txt in self.get_mapping().items() if opt in opts}
        )


class OptionDisplayText(object):
    """Class for containing all of the display text listings."""

    agent_options = DisplayTextListing(
        {
            AgentOptions.value_iteration_optimised: "Value Iteration",
            AgentOptions.q_learning: "Q-Learning",
        }
    )

    full_exploration_options = DisplayTextListing(
        {
            ExplorationStrategyOptions.not_applicable: "Not Applicable",
            ExplorationStrategyOptions.epsilon_greedy: "Epsilon Greedy",
            ExplorationStrategyOptions.upper_confidence_bound: (
                "(UCB) Upper Confidence Bound"
            ),
            ExplorationStrategyOptions.mf_bpi: (
                "(MF-BPI) Model-Free Best Policy Identification"
            ),
        }
    )

    not_applicable_exploration_option = full_exploration_options.create_subset(
        ExplorationStrategyOptions.not_applicable
    )

    applicable_exploration_option = full_exploration_options.create_subset(
        ExplorationStrategyOptions.epsilon_greedy,
        ExplorationStrategyOptions.upper_confidence_bound,
        ExplorationStrategyOptions.mf_bpi,
    )

    dynamics_options = DisplayTextListing(
        {
            DynamicsOptions.collection: "Collection",
            DynamicsOptions.cliff: "Cliff",
            DynamicsOptions.wind: "Wind",
        }
    )

    display_mode_options = DisplayTextListing(
        {
            DisplayMode.default: "default",
            DisplayMode.best_action: "best action",
            DisplayMode.state_value: "state value",
            DisplayMode.action_value_global: "action value",
            DisplayMode.action_value_local: "action value local",
        }
    )

    auto_speed_options = DisplayTextListing(
        {
            AutomaticOptions.manual: "Manual",
            AutomaticOptions.automatic_playing: "Auto",
            AutomaticOptions.automatic_paused: "Auto (paused)",
        }
    )

    auto_selector_options = auto_speed_options.create_subset(
        AutomaticOptions.manual, AutomaticOptions.automatic_playing
    )

    progress_button_text = DisplayTextListing(
        {
            AutomaticOptions.manual: "Next",
            AutomaticOptions.automatic_playing: "Pause",
            AutomaticOptions.automatic_paused: "Play",
        }
    )
