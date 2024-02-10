from dataclasses import dataclass

from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.learning_system.top_level_entities.options import (
    AgentOptions,
    DynamicsOptions,
    TopEntitiesOptions,
)


@dataclass(frozen=True, slots=True)
class HyperParameterDescription(object):
    """Defines the meta information about a hyper parameter.

    such as range of sensible values for a hyper parameter.
    """

    min_value: float
    max_value: float
    tuning_options: TopEntitiesOptions
    integer_valued: bool = False

    def cap_samples(self, samples: int) -> int:
        """Cap the number of samples for integer ranges to avoid oversampling.

        Args:
            samples (int): the intended number of samples before the cap

        Returns:
            int: the number of samples in the range after adjustment.
        """
        if not self.integer_valued:
            return samples

        interval = int(self.max_value - self.min_value)
        return min(interval, samples)

    def interpolate_value(self, factor: float) -> float:
        """Interpolate in the range with the given factor.

        Args:
            factor (float): the factor of the way through the range. typically
                between zero and one.

        Returns:
            float: the value in the range based on this factor.
        """
        interval = self.max_value - self.min_value
        interpolated_value = interval * factor + self.min_value

        if not self.integer_valued:
            return interpolated_value
        return round(interpolated_value)


class TuningInformation(object):
    """Class for containing the meta information about tuning parameters."""

    eg_options = TopEntitiesOptions(
        AgentOptions.q_learning,
        DynamicsOptions.cliff,
        ExplorationStrategyOptions.epsilon_greedy,
    )

    ucb_options = TopEntitiesOptions(
        AgentOptions.q_learning,
        DynamicsOptions.cliff,
        ExplorationStrategyOptions.upper_confidence_bound,
    )

    parameter_details = {
        HyperParameter.initial_optimism: HyperParameterDescription(
            -10, 10, eg_options
        ),
        HyperParameter.replay_queue_length: HyperParameterDescription(
            0, 10, eg_options, integer_valued=True
        ),
        HyperParameter.learning_rate: HyperParameterDescription(
            0.1**3,
            0.1,
            eg_options,
        ),
        HyperParameter.discount_rate: HyperParameterDescription(
            0.5, 1, eg_options
        ),
        HyperParameter.eg_exploration_ratio: HyperParameterDescription(
            0, 1, eg_options
        ),
        HyperParameter.ucb_exploration_bias: HyperParameterDescription(
            0, 5, ucb_options
        ),
    }

    @classmethod
    def tunable_parameters(cls) -> set[HyperParameter]:
        """Get all parameters that are tunable.

        Returns:
            set[HyperParameter]: the parameters that can be tuned.
        """
        return set(cls.parameter_details.keys())

    @classmethod
    def get_parameter_details(
        cls, parameter: HyperParameter
    ) -> HyperParameterDescription:
        """Get the tuning information of a given parameter.

        Args:
            parameter (HyperParameter): the parameter to be tuned

        Raises:
            ValueError: if the parameter should not be tuned.

        Returns:
            HyperParameterDescription: the meta information about this parameter
        """
        details = cls.parameter_details.get(parameter, None)

        if details is None:
            raise ValueError(
                f"parameter {parameter.name} is not valid for tuning."
            )

        return details
