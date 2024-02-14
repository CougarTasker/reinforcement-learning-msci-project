from typing import Dict

from typing_extensions import override

from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
    HyperParameter,
)
from src.model.hyperparameters.tuning_information import TuningInformation


class RandomParameterStrategy(BaseHyperParameterStrategy):
    """This class provides hyperparameter values from the configuration."""

    def __init__(self) -> None:
        """Initialise the parameter manager.

        This is where the parameter manager picks the random values
        """
        self.parameter_values = {
            hyper_parameter: TuningInformation.get_parameter_details(
                hyper_parameter
            ).get_random_value()
            for hyper_parameter in TuningInformation.tunable_parameters()
        }

    def get_parameters(self) -> Dict[HyperParameter, float]:
        """Get the parameters used by this strategy.

        Returns:
            Dict[HyperParameter, float]: the parameter values
        """
        return self.parameter_values

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
        parameter_value = self.parameter_values.get(parameter, None)
        if parameter_value is None:
            raise ValueError(f'parameter "{parameter.name}" is not known')
        return parameter_value
