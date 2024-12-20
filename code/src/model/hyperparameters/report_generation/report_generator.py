from itertools import repeat
from multiprocessing import Manager, Pool, Process
from typing import Tuple

import numpy as np

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.parameter_evaluator import ParameterEvaluator
from src.model.hyperparameters.tuning_information import TuningInformation

from .compute_confidence_interval import compute_confidence_interval
from .report_data import HyperParameterReport, ReportState
from .tuning_parameter_strategy import ParameterTuningStrategy


class HyperParameterReportGenerator(object):
    """Class for creating hyper parameter tuning reports."""

    worker_count = 8
    iterations_per_worker = 1000
    samples = 100
    runs = 25

    def __init__(self) -> None:
        """Initialise the report generator."""
        manager = Manager()

        self.state = manager.Value(ReportState, ReportState(None, {}, {}))
        self.state_lock = manager.Lock()

        self.running = manager.Value(bool, value=True)

    def shutdown(self):
        """Abort any existing work, Stop child processes."""
        self.running.set(False)

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
        run_progress = 1 / (samples * self.runs)

        with Pool(processes=self.worker_count) as pool:
            simulation_results = pool.starmap(
                self.evaluate_value,
                zip(repeat(parameter), x_axis, repeat(run_progress)),
            )
            if not self.running:
                return

            lower_bounds, y_axis, upper_bounds = map(
                list, zip(*simulation_results)
            )

            report = HyperParameterReport(
                parameter, x_axis, lower_bounds, y_axis, upper_bounds
            )

            with self.state_lock:
                state = self.state.get()
                self.state.set(state.complete_request(report))

    confidence_level = 0.95
    confidence_iterations = 1000

    def evaluate_value(
        self,
        parameter: HyperParameter,
        parameter_value: float,
        run_progress_amount: float,
    ) -> Tuple[float, float, float]:
        """Evaluate a parameter and value combination.

        Args:
            parameter (HyperParameter): the parameter to test
            parameter_value (float): the value for this parameter to assume
            run_progress_amount (float): the amount of progress made in a single
                run.

        Returns:
            float: the total reward under these conditions.
        """
        # skip computation if shutting down.
        details = TuningInformation.get_parameter_details(parameter)
        hyper_parameters = ParameterTuningStrategy(parameter, parameter_value)

        rewards = []

        for _ in range(self.runs):
            if not self.running.get():
                return 0, 0, 0
            stats = ParameterEvaluator.single_run(
                details.tuning_options, hyper_parameters
            )
            rewards.append(stats.total_reward)

            with self.state_lock:
                state = self.state.get()
                new_progress = (
                    state.pending_requests.get(parameter, 1)
                    + run_progress_amount
                )
                self.state.set(
                    state.update_report_progress(parameter, new_progress)
                )

        return compute_confidence_interval(
            np.array(rewards, dtype=np.float64),
            self.confidence_level,
            self.confidence_iterations,
        )
