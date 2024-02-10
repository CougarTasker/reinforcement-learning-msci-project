from ..base_section import BaseConfigSection


class EpsilonGreedyStrategyConfig(BaseConfigSection):
    """Gets configuration related to the epsilon greedy exploration strategy."""

    exploration_ratio_property = "exploration_ratio"

    def __init__(self) -> None:
        """Instantiate epsilon greedy section config."""
        data_schema = {
            self.exploration_ratio_property: float,
        }

        super().__init__("epsilon_greedy", data_schema, [])

    @property
    def exploration_ratio(self) -> float:
        """Get the ratio the agent should explore vs exploit.

        also known as epsilon in epsilon greedy and soft strategies

        Returns:
            float: the ratio for exploring, 1 represents always exploring. 0
                never exploring.
        """
        return self.configuration[self.exploration_ratio_property]
