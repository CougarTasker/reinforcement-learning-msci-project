from typing import Optional

from typing_extensions import override

from src.model.config.agent_section.agent_section import AgentConfig
from src.model.config.reader import ConfigReader
from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
    HyperParameter,
)


class ParameterConfigStrategy(BaseHyperParameterStrategy):
    """This class provides hyperparameter values from the configuration."""

    def __init__(self, agent_config: Optional[AgentConfig] = None) -> None:
        """Initialise the parameter manager.

        Args:
            agent_config (Optional[AgentConfig]): the configuration reader the
                hyper-parameters should use, if not provided the default one
                will be used.
        """
        super().__init__()
        if agent_config is None:
            agent_config = ConfigReader().agent
        q_learning_config = agent_config.q_learning
        value_iteration_config = agent_config.value_iteration

        self.parameter_values = {
            HyperParameter.initial_optimism: q_learning_config.initial_optimism,
            HyperParameter.replay_queue_length: (
                q_learning_config.replay_queue_length
            ),
            HyperParameter.learning_rate: q_learning_config.learning_rate,
            HyperParameter.discount_rate: agent_config.discount_rate,
            HyperParameter.eg_initial_exploration_ratio: (
                q_learning_config.epsilon_greedy.initial_exploration_ratio
            ),
            HyperParameter.eg_decay_rate: (
                q_learning_config.epsilon_greedy.decay_rate
            ),
            HyperParameter.ucb_exploration_bias: (
                q_learning_config.upper_confidence_bound.exploration_bias
            ),
            HyperParameter.stopping_epsilon: (
                value_iteration_config.stopping_epsilon
            ),
            HyperParameter.sample_count: value_iteration_config.sample_count,
            HyperParameter.mf_error_sensitivity: (
                q_learning_config.mf_bpi.error_sensitivity
            ),
            HyperParameter.mf_bpi_ensemble_size: (
                q_learning_config.mf_bpi.ensemble_size
            ),
            HyperParameter.mf_exploration_parameter: (
                q_learning_config.mf_bpi.exploration_parameter
            ),
        }

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
