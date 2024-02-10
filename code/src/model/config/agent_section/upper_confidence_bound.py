from ..base_section import BaseConfigSection


class UCBStrategyConfig(BaseConfigSection):
    """Gets configuration related to the UCB exploration strategy."""

    exploration_bias_property = "exploration_bias"

    def __init__(self) -> None:
        """Instantiate upper confidence bound section config."""
        data_schema = {
            self.exploration_bias_property: float,
        }

        super().__init__("upper_confidence_bound", data_schema, [])

    @property
    def exploration_bias(self) -> float:
        """Weighting applied to the uncertainty in the recorded data.

        Higher values encourage more exploration.

        Returns:
            float: The value of potential reward.
        """
        return self.configuration[self.exploration_bias_property]
