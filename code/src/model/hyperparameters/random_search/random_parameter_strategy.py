from typing import Dict, Optional

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
        # make the parameters are demand driven to avoid redundant values.
        self.parameter_values: Dict[HyperParameter, Optional[float]] = {
            parameter: None
            for parameter in TuningInformation.tunable_parameters()
        }

    def get_parameters(self) -> Dict[HyperParameter, Optional[float]]:
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
        if parameter not in TuningInformation.tunable_parameters():
            raise ValueError(f'parameter "{parameter.name}" is not known')

        parameter_value = self.parameter_values.get(parameter, None)
        if parameter_value is not None:
            return parameter_value

        new_value = TuningInformation.get_parameter_details(
            parameter
        ).get_random_value()
        self.parameter_values[parameter] = new_value
        return new_value
