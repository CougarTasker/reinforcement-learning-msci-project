from schema import Schema

from .base_section import BaseConfigSection


class AgentConfig(BaseConfigSection):
    """Gets configuration related to the GUI."""

    discount_rate_property = "discount_rate"
    stopping_epsilon_property = "stopping_epsilon"
    learning_rate_property = "learning_rate"
    sample_count_property = "sample_count"
    exploration_ratio_property = "exploration_ratio"

    def __init__(self) -> None:
        """Instantiate Grid world section config."""
        data_schema = Schema(
            {
                self.discount_rate_property: float,
                self.stopping_epsilon_property: float,
                self.learning_rate_property: float,
                self.sample_count_property: int,
                self.exploration_ratio_property: float,
            }
        )
        super().__init__("agent", data_schema)

    def discount_rate(self) -> float:
        """Get the discount rate.

        Returns:
            float: the amount to discount future reward
        """
        return self.configuration[self.discount_rate_property]

    def stopping_epsilon(self) -> float:
        """Get the stopping epsilon.

        Returns:
            float: the maximum error allowable in a value table
        """
        return self.configuration[self.stopping_epsilon_property]

    def learning_rate(self) -> float:
        """Get the learning rate.

        Returns:
            float: the amount to update the value table with each observation
        """
        return self.configuration[self.learning_rate_property]

    def sample_count(self) -> int:
        """Get the sample count.

        Returns:
            int: the number of samples to use for distribution analysis.
        """
        return self.configuration[self.sample_count_property]

    def exploration_ratio(self) -> float:
        """Get the ratio the agent should explore vs exploit.

        also known as epsilon in epsilon greedy and soft strategies

        Returns:
            float: the ratio for exploring, 1 represents always exploring. 0
            never exploring.
        """
        return self.configuration[self.exploration_ratio_property]
