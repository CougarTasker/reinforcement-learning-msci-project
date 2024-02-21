from multiprocessing.managers import ValueProxy

from src.model.hyperparameters.base_parameter_strategy import (
    BaseHyperParameterStrategy,
)
from src.model.learning_system.learning_instance.learning_instance import (
    LearningInstance,
)
from src.model.learning_system.learning_instance.statistics_record import (
    StatisticsRecord,
)
from src.model.learning_system.top_level_entities.factory import EntityFactory
from src.model.learning_system.top_level_entities.options import (
    TopEntitiesOptions,
)


class ParameterEvaluator(object):
    """This class simulations and evaluates different configurations."""

    runs = 5
    iterations_per_run = 1500

    @classmethod
    def evaluate_reward(
        cls,
        options: TopEntitiesOptions,
        hyper_parameters: BaseHyperParameterStrategy,
        running: ValueProxy[bool],
    ) -> float:
        """Evaluate the reward of a given configuration.

        this method will evaluate the reward multiple times and average out the
        value to reduce noise in the recording.

        Args:
            options (TopEntitiesOptions): The major non-tunable configuration.
            hyper_parameters (BaseHyperParameterStrategy): the hyper parameters
                to use.
            running (ValueProxy[bool]): a value to determine early stopping.

        Returns:
            float: The average total reward for a given configuration.
        """
        total_reward = float(0)

        for _ in range(cls.runs):
            if not running.get():
                return -float("inf")
            total_reward += cls.single_run(
                options, hyper_parameters
            ).total_reward

        return total_reward / cls.runs

    @classmethod
    def single_run(
        cls,
        options: TopEntitiesOptions,
        hyper_parameters: BaseHyperParameterStrategy,
    ) -> StatisticsRecord:
        """Perform a single simulated run.

        Args:
            options (TopEntitiesOptions): the top options for this run
            hyper_parameters (BaseHyperParameterStrategy): the parameters to
                use.

        Returns:
            StatisticsRecord: the statistics from this run.
        """
        entities = EntityFactory.create_entities(options, hyper_parameters)

        learning_instance = LearningInstance(entities)

        for _ in range(cls.iterations_per_run):
            learning_instance.perform_action()
        return entities.statistics.get_statistics()
