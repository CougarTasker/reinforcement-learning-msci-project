from enum import Enum


class HyperParameter(Enum):
    """Enumerates all the different hyperparameters."""

    initial_optimism = 0
    replay_queue_length = 1
    learning_rate = 2
    discount_rate = 3
    eg_initial_exploration_ratio = 4
    eg_decay_rate = 5
    ucb_exploration_bias = 6
    stopping_epsilon = 7
    sample_count = 8
    mf_bpi_kbar = 9
    mf_bpi_ensemble_size = 10


class BaseHyperParameterStrategy(object):
    """The base class for hyper parameter managers."""

    def get_value(self, parameter: HyperParameter) -> float:
        """Get the given hyper-parameter's value.

        Args:
            parameter (HyperParameter): Specifies which parameter to use.

        Raises:
            NotImplementedError: If not overridden by a concrete class

        Returns:
            float: The value of this hyper parameter.
        """
        self.__raise_not_implemented()
        return 0

    def get_integer_value(self, parameter: HyperParameter) -> int:
        """Get the value of a hyper parameter that is an integer.

        Args:
            parameter (HyperParameter): Specifies which parameter to use.

        Raises:
            TypeError: If the parameter's value is not an integer.

        Returns:
            int: The value of this hyper parameter.
        """
        parameter_value = self.get_value(parameter)
        # unfortunately this is one of the best ways to do this in python.
        int_parameter_value = int(parameter_value)
        if int_parameter_value == parameter_value:
            return int_parameter_value

        raise TypeError(
            f"parameter {parameter.name} did not have an integer type \n"
        )

    def __raise_not_implemented(self):
        raise NotImplementedError(
            "Concrete classes should override this method."
        )
