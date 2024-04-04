from ..base_section import BaseConfigSection


class MFBPIConfig(BaseConfigSection):
    """Gets configuration related to the value iteration agent."""

    error_sensitivity_property = "error_sensitivity"
    ensemble_size_property = "ensemble_size"
    exploration_parameter_property = "exploration_parameter"

    def __init__(self) -> None:
        """Instantiate value iteration section config."""
        data_schema = {
            self.error_sensitivity_property: int,
            self.ensemble_size_property: int,
            self.exploration_parameter_property: float,
        }

        super().__init__("mf_bpi", data_schema, [])

    @property
    def error_sensitivity(self) -> int:
        """Get the error sensitivity. Measure that effects uncertainty.

        higher error sensitivity increases uncertainty, therefore more
        exploration. although becomes more sensitive to noise.

        Returns:
            int: the sensitivity to TD errors.
        """
        return self.configuration[self.error_sensitivity_property]

    @property
    def ensemble_size(self) -> int:
        """Get the number of Q-value tables to maintain in the ensemble.

        Returns:
            int: the number of Q-value tables.
        """
        return self.configuration[self.ensemble_size_property]

    @property
    def exploration_parameter(self) -> float:
        """Get the amount of forced exploration.

        Recommended value is 1, higher values equate to more exploration.

        Returns:
            float: exploration amount.
        """
        return self.configuration[self.ensemble_size_property]
