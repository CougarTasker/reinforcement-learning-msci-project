from src.model.config.agent_section.q_learning import QLearningConfig
from src.model.config.agent_section.value_iteration import ValueIterationConfig

from ..base_section import BaseConfigSection


class AgentConfig(BaseConfigSection):
    """Gets configuration related to agents."""

    discount_rate_property = "discount_rate"

    def __init__(self) -> None:
        """Instantiate agent section config."""
        data_schema = {
            self.discount_rate_property: float,
        }
        self.q_learning = QLearningConfig()
        self.value_iteration = ValueIterationConfig()

        super().__init__(
            "agent",
            data_schema,
            [self.q_learning, self.value_iteration],
        )

    @property
    def discount_rate(self) -> float:
        """Get the discount rate.

        Returns:
            float: the amount to discount future reward
        """
        return self.configuration[self.discount_rate_property]
