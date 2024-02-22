from ..base_section import BaseConfigSection


class MFBPIConfig(BaseConfigSection):
    """Gets configuration related to the value iteration agent."""

    kbar_property = "kbar"
    ensemble_size_property = "ensemble_size"

    def __init__(self) -> None:
        """Instantiate value iteration section config."""
        data_schema = {
            self.kbar_property: int,
            self.ensemble_size_property: int,
        }

        super().__init__("mf_bpi", data_schema, [])

    @property
    def kbar(self) -> int:
        """Get the kbar.

        Not sure what the kbar is but it is used in initialisation and is just
        set to one by the authors.

        Returns:
            int: unknown meaning.
        """
        return self.configuration[self.kbar_property]

    @property
    def ensemble_size(self) -> int:
        """Get the number of Q-value tables to maintain in the ensemble.

        Returns:
            int: the number of Q-value tables.
        """
        return self.configuration[self.ensemble_size_property]
