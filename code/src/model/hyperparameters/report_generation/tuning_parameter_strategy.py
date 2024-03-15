from typing_extensions import override

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.config_parameter_strategy import (
    ParameterConfigStrategy,
)


class ParameterTuningStrategy(ParameterConfigStrategy):
    """This class provides hyperparameter values with the tuning adjustment."""

    def __init__(
        self, tuning_parameter: HyperParameter, parameter_value: float
    ) -> None:
        """Initialise the parameter manager.

        Args:
            tuning_parameter (HyperParameter): the parameter that should be
                varied.
            parameter_value (float): the set value of this parameter.
        """
        super().__init__()
        self.tuning_parameter = tuning_parameter
        self.parameter_value = parameter_value

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

        return self.parameter_value
