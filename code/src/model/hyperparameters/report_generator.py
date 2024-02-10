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

    worker_count = 5
    iterations_per_worker = 100
    samples = 10

    def __init__(self) -> None:
        """Initialise the report generator."""
        manager = Manager()

        self.state = manager.Value(ReportState, ReportState(set(), {}))
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
            # skip redundant work.
            if parameter in state.pending_requests:
                return
            if parameter in state.available_reports:
                return
            self.state.set(state.add_pending_request(parameter))

        generator = Process(
            target=self.__generate_report_thread,
            name=f"report-generator {parameter.name}",
            args=(parameter,),
        )
        generator.start()

    def __generate_report_thread(self, parameter: HyperParameter):
        details = TuningInformation.get_parameter_details(parameter)
        samples = details.cap_samples(self.samples)
        progress_steps = np.linspace(0, 1, samples)
        interpolate = np.vectorize(details.interpolate_value)
        x_axis = interpolate(progress_steps)

        with Pool(processes=self.worker_count) as pool:
            y_axis = pool.starmap(
                self.__test_value, zip(repeat(parameter), x_axis)
            )

            report = HyperParameterReport(parameter, x_axis, y_axis)

            with self.state_lock:
                state = self.state.get()
                self.state.set(state.complete_request(report))

    def __test_value(
        self, parameter: HyperParameter, parameter_value: float
    ) -> float:
        details = TuningInformation.get_parameter_details(parameter)
        hyper_parameters = ParameterTuningStrategy(parameter, parameter_value)
        entities = EntityFactory.create_entities(
            details.tuning_options, hyper_parameters
        )

        learning_instance = LearningInstance(entities)

        for _ in range(self.iterations_per_worker):
            learning_instance.perform_action()

        return entities.statistics.get_statistics().total_reward
