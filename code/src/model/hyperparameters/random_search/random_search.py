from multiprocessing import Manager, Process
from typing import Dict

from src.model.agents.q_learning.exploration_strategies.options import (
    ExplorationStrategyOptions,
)
from src.model.hyperparameters.config_parameter_strategy import (
    ParameterConfigStrategy,
)
from src.model.hyperparameters.parameter_evaluator import ParameterEvaluator
from src.model.hyperparameters.random_search.random_parameter_strategy import (
    RandomParameterStrategy,
)
from src.model.hyperparameters.random_search.random_search_data import (
    RandomSearchState,
    SearchArea,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.model.learning_system.top_level_entities.options import (
    AgentOptions,
    DynamicsOptions,
    TopEntitiesOptions,
)


class RandomSearch(object):
    """Class for performing a random search."""

    worker_count = 8
    iterations_per_worker = 1000
    runs = 5

    def __init__(self) -> None:
        """Initialise random search runner."""
        manager = Manager()

        self.search_options = [
            TopEntitiesOptions(
                AgentOptions.q_learning,
                DynamicsOptions.cliff,
                ExplorationStrategyOptions.epsilon_greedy,
            ),
            TopEntitiesOptions(
                AgentOptions.q_learning,
                DynamicsOptions.collection,
                ExplorationStrategyOptions.epsilon_greedy,
            ),
            TopEntitiesOptions(
                AgentOptions.q_learning,
                DynamicsOptions.cliff,
                ExplorationStrategyOptions.upper_confidence_bound,
            ),
            TopEntitiesOptions(
                AgentOptions.q_learning,
                DynamicsOptions.collection,
                ExplorationStrategyOptions.upper_confidence_bound,
            ),
        ]

        initial_params = {
            tunable_parameter: None
            for tunable_parameter in TuningInformation.tunable_parameters()
        }

        initial_data = RandomSearchState(
            None,
            {
                options: SearchArea(options, initial_params, None, 0)
                for options in self.search_options
            },
            searching=False,
        )
        self.state = manager.Value(RandomSearchState, initial_data)

        self.state_lock = manager.Lock()

        self.running = manager.Value(bool, value=False)

    def get_progress(self) -> RandomSearchState:
        """Get the current state of the search if there is one.

        Returns:
            RandomSearchState: the current result of the search.
        """
        with self.state_lock:
            return self.state.value

    def start_search(self):
        """Start the searching process."""
        with self.state_lock:
            if self.running.get():
                return
            self.running.set(True)
            self.state.set(self.state.get().set_searching(True))

        optimal_runner = Process(
            target=self.run_optimal_search, name="optimal rewards search"
        )
        optimal_runner.start()

        for runner_id in range(self.worker_count):
            search_runner = Process(
                target=self.run_search_inner,
                name=f"random search runner {runner_id}",
            )
            search_runner.start()

    def stop_search(self):
        """Stop the searching process."""
        self.running.set(False)
        with self.state_lock:
            self.state.set(self.state.get().set_searching(False))

    def run_optimal_search(self):
        """Run a search for the optimal reward under the given conditions.

        This is done with value iteration.
        """
        optimal_rewards: Dict[DynamicsOptions, float] = {}
        for dynamics in DynamicsOptions:
            if not self.running.get():
                return
            options = TopEntitiesOptions(
                AgentOptions.value_iteration_optimised,
                dynamics,
                ExplorationStrategyOptions.not_applicable,
            )
            normal_parameters = ParameterConfigStrategy()
            optimal_rewards[dynamics] = ParameterEvaluator.evaluate_reward(
                options, normal_parameters, self.running
            )
        if not self.running.get():
            return

        with self.state_lock:
            state = self.state.get()
            self.state.set(state.set_optimal_rewards(optimal_rewards))

    def run_search_inner(self):
        """Run the actual search.

        this method is used internally please use `start_search` to actually
        start the search from another class.
        """
        while self.running.get():
            for options in self.search_options:
                if not self.running.get():
                    return
                hyper_parameters = RandomParameterStrategy()

                total_reward = ParameterEvaluator.evaluate_reward(
                    options, hyper_parameters, self.running
                )

                if not self.running.get():
                    return

                with self.state_lock:
                    state = self.state.get()
                    self.state.set(
                        state.record_result(
                            options, hyper_parameters, total_reward
                        )
                    )
