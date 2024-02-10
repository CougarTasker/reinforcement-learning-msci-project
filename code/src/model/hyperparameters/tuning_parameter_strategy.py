from dataclasses import dataclass

from typing_extensions import override

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.config_parameter_strategy import (
    ParameterConfigStrategy,
)


@dataclass(frozen=True, slots=True)
class HyperParameterDescription(object):
    """Defines the meta information about a hyper parameter.

    such as range of sensible values for a hyper parameter.
    """

    min_value: float
    max_value: float
    integer_valued: bool = False

    def minimum_step_size(self) -> float:
        """Provide the minimal step size for iterating over this range.

        This step size will avoid oversampling of an integer range.

        Returns:
            float: the minimum step size for the range
        """
        if self.integer_valued:
            return 1 / (self.max_value - self.min_value)
        return 0

    def interpolate_value(self, factor: float) -> float:
        """Interpolate in the range with the given factor.

        Args:
            factor (float): the factor of the way through the range. typically
                between zero and one.

        Returns:
            float: the value in the range based on this factor.
        """
        return (self.max_value - self.min_value) * factor + self.min_value


class ParameterTuningStrategy(ParameterConfigStrategy):
    """This class provides hyperparameter values with the tuning adjustment."""

    parameter_details = {
        HyperParameter.initial_optimism: HyperParameterDescription(-10, 10),
        HyperParameter.replay_queue_length: HyperParameterDescription(
            0, 10, integer_valued=True
        ),
        HyperParameter.learning_rate: HyperParameterDescription(0.1**3, 0.1),
        HyperParameter.discount_rate: HyperParameterDescription(0.5, 1),
        HyperParameter.eg_exploration_ratio: HyperParameterDescription(0, 1),
        HyperParameter.ucb_exploration_bias: HyperParameterDescription(0, 5),
    }

    def __init__(
        self, tuning_parameter: HyperParameter, progress: float
    ) -> None:
        """Initialise the parameter manager.

        Args:
            tuning_parameter (HyperParameter): the parameter that should be
                varied.
            progress (float): the progress through the range for this instance.
                this is a float value in the range zero to one.
        """
        super().__init__()
        self.tuning_parameter = tuning_parameter

        tuning_details = self.parameter_details[tuning_parameter]

        self.tuning_value = tuning_details.interpolate_value(progress)

        if tuning_details.integer_valued:
            self.tuning_value = int(round(self.tuning_value))

    @override
    def get_value(self, parameter: HyperParameter) -> float:
        """Get the value of a given hyper parameter.

        Args:
            parameter (HyperParameter): the parameter to access.

        Raises:
            ValueError: if the parameter provided is not known.

        Returns:
            float: the value of this parameter.
        """
        if parameter is not self.tuning_parameter:
            return super().get_value(parameter)

        return self.tuning_value
