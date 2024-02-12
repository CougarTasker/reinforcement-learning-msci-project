from itertools import repeat
from multiprocessing import Manager, Pool, Process

import numpy as np

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.report_data import (
    HyperParameterReport,
    ReportState,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.model.hyperparameters.tuning_parameter_strategy import (
    ParameterTuningStrategy,
)
from src.model.learning_system.learning_instance.learning_instance import (
    LearningInstance,
)
from src.model.learning_system.top_level_entities.factory import EntityFactory


class HyperParameterReportGenerator(object):
    """Class for creating hyper parameter tuning reports."""

    worker_count = 8
    iterations_per_worker = 100
    samples = 100
    runs = 5

    def __init__(self) -> None:
        """Initialise the report generator."""
        manager = Manager()

        self.state = manager.Value(ReportState, ReportState(None, {}, {}))
        self.state_lock = manager.Lock()

    def get_state(self) -> ReportState:
        """Get the current state of the reports.

        Returns:
            ReportState: the current state of the reports.
        """
        with self.state_lock:
            return self.state.value

    def generate_report(self, parameter: HyperParameter):
        """Generate a report about a given hyper parameter.

        Args:
            parameter (HyperParameter): the parameter to create the report for.

        Raises:
            ValueError: if the parameter is not valid for report generation.
        """
        if parameter not in TuningInformation.tunable_parameters():
            raise ValueError(
                f"parameter {parameter.name} is not valid for tuning."
            )
        with self.state_lock:
            state = self.state.get()
            self.state.set(state.report_requested(parameter))

            pending = parameter in state.pending_requests
            available = parameter in state.available_reports

            if pending or available:
                # skip redundant information
                return

        generator = Process(
            target=self.generate_report_worker,
            name=f"report-generator {parameter.name}",
            args=(parameter,),
        )
        generator.start()

    def generate_report_worker(self, parameter: HyperParameter):
        """Generate a report for a given parameter.

        this is the internal method that does the heavy lifting in a separate
        thread. the public method should do all of the validation.

        Args:
            parameter (HyperParameter): the parameter to evaluate
        """
        details = TuningInformation.get_parameter_details(parameter)
        samples = details.cap_samples(self.samples)
        progress_steps = np.linspace(0, 1, samples)
        interpolate = np.vectorize(details.interpolate_value)
        x_axis = interpolate(progress_steps)

        with Pool(processes=self.worker_count) as pool:
            y_axis = pool.starmap(
                self.evaluate_value, zip(repeat(parameter), x_axis)
            )

            report = HyperParameterReport(parameter, x_axis, y_axis)

            with self.state_lock:
                state = self.state.get()
                self.state.set(state.complete_request(report))

    def evaluate_value(
        self, parameter: HyperParameter, parameter_value: float
    ) -> float:
        """Evaluate a parameter and value combination.

        Args:
            parameter (HyperParameter): the parameter to test
            parameter_value (float): the value for this parameter to assume

        Returns:
            float: the total reward under these conditions.
        """
        details = TuningInformation.get_parameter_details(parameter)
        hyper_parameters = ParameterTuningStrategy(parameter, parameter_value)

        total_reward = 0

        run_progress_amount = 1 / (self.samples * self.runs)

        for _ in range(self.runs):
            entities = EntityFactory.create_entities(
                details.tuning_options, hyper_parameters
            )

            learning_instance = LearningInstance(entities)

            for _ in range(self.iterations_per_worker):
                learning_instance.perform_action()
            stats = entities.statistics.get_statistics()
            total_reward += stats.total_reward

            with self.state_lock:
                state = self.state.get()
                new_progress = (
                    state.pending_requests.get(parameter, 1)
                    + run_progress_amount
                )
                self.state.set(
                    state.update_report_progress(parameter, new_progress)
                )
        return total_reward / self.runs
