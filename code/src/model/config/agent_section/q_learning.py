from src.model.config.agent_section.epsilon_greedy import (
    EpsilonGreedyStrategyConfig,
)
from src.model.config.agent_section.mf_bpi import MFBPIConfig
from src.model.config.agent_section.upper_confidence_bound import (
    UCBStrategyConfig,
)

from ..base_section import BaseConfigSection


class QLearningConfig(BaseConfigSection):
    """Gets configuration related to Q learning."""

    learning_rate_property = "learning_rate"
    initial_optimism_property = "initial_optimism"
    replay_queue_length_property = "replay_queue_length"

    def __init__(self) -> None:
        """Instantiate q-learning section config."""
        data_schema = {
            self.learning_rate_property: float,
            self.initial_optimism_property: float,
            self.replay_queue_length_property: int,
        }

        self.epsilon_greedy = EpsilonGreedyStrategyConfig()
        self.upper_confidence_bound = UCBStrategyConfig()
        self.mf_bpi = MFBPIConfig()
        super().__init__(
            "q_learning",
            data_schema,
            [self.epsilon_greedy, self.upper_confidence_bound, self.mf_bpi],
        )

    @property
    def learning_rate(self) -> float:
        """Get the learning rate.

        Returns:
            float: the amount to update the value table with each observation
        """
        return self.configuration[self.learning_rate_property]

    @property
    def initial_optimism(self) -> float:
        """Get the initial optimism of the value table.

        this is the average value of the initial guess of the q-value table
        before any data has been collected. Could be negative for a pessimistic
        world view.

        Returns:
            float: The average value in the value table initially.
        """
        return self.configuration[self.initial_optimism_property]

    @property
    def replay_queue_length(self) -> int:
        """Get the number of previous actions to retain in the replay queue.

        Returns:
            int: the maximum size of the replay queue.
        """
        return self.configuration[self.replay_queue_length_property]
