from ..base_section import BaseConfigSection


class EpsilonGreedyStrategyConfig(BaseConfigSection):
    """Gets configuration related to the epsilon greedy exploration strategy."""

    exploration_ratio_property = "initial_exploration_ratio"
    decay_rate_property = "decay_rate"

    def __init__(self) -> None:
        """Instantiate epsilon greedy section config."""
        data_schema = {
            self.exploration_ratio_property: float,
            self.decay_rate_property: float,
        }

        super().__init__("epsilon_greedy", data_schema, [])

    @property
    def initial_exploration_ratio(self) -> float:
        """Get the ratio the agent should explore vs exploit initially.

        also known as epsilon in epsilon greedy and soft strategies

        Returns:
            float: the ratio for exploring, 1 represents always exploring. 0
                never exploring.
        """
        return self.configuration[self.exploration_ratio_property]

    @property
    def decay_rate(self) -> float:
        """Get the rate at witch the exploration rate should decay.

        Returns:
            float: the ratio for decay, 1 represents no decay 0.1 represents a
                quick decay.
        """
        return self.configuration[self.decay_rate_property]
