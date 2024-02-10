from ..base_section import BaseConfigSection


class ValueIterationConfig(BaseConfigSection):
    """Gets configuration related to the value iteration agent."""

    sample_count_property = "sample_count"
    stopping_epsilon_property = "stopping_epsilon"

    def __init__(self) -> None:
        """Instantiate value iteration section config."""
        data_schema = {
            self.stopping_epsilon_property: float,
            self.sample_count_property: int,
        }

        super().__init__("value_iteration", data_schema, [])

    @property
    def stopping_epsilon(self) -> float:
        """Get the stopping epsilon.

        Returns:
            float: the maximum error allowable in a value table
        """
        return self.configuration[self.stopping_epsilon_property]

    @property
    def sample_count(self) -> int:
        """Get the sample count.

        Returns:
            int: the number of samples to use for distribution analysis.
        """
        return self.configuration[self.sample_count_property]
