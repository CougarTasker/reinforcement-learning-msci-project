from multiprocessing import Process
from time import time
from typing import Optional

from typing_extensions import Self

from src.controller.hyper_parameter_controller.request_bridge import (
    HyperParameterRequest,
    HyperParameterRequestBridge,
    ReportRequestMessage,
)
from src.controller.hyper_parameter_controller.update_bridge import (
    HyperParameterUpdateBridge,
)
from src.model.hyperparameters.hyper_parameter_system import (
    HyperParameterSystem,
)


class HyperParameterController(object):
    """Controller for managing the hyper parameter functionality."""

    minimum_update_delta_seconds = 0.3

    def __init__(self) -> None:
        """Initialise the learning system controller."""
        self.system = HyperParameterSystem()

        self.request_bridge = HyperParameterRequestBridge()
        self.update_bridge = HyperParameterUpdateBridge()

        self.report_process: Optional[Process] = None

        self.last_update_timestamp = time()

    def __enter__(self) -> Self:
        """Enter the context manager.

        the context manager is used for cleaning up processes gracefully.

        Returns:
            Self: the factory.
        """
        self.report_process = Process(
            target=self.report_mainloop, name="report_mainloop"
        )
        self.report_process.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """Exit the context, clean up the resources.

        Args:
            exc_type (Any): Not used.
            exc_value (Any): Not used.
            exc_tb (Any): Not used.
        """
        self.request_bridge.request_shutdown()
        if self.report_process is not None:
            self.report_process.join()

    def report_mainloop(
        self,
    ):
        """Run the main loop of the report generation process.

        Raises:
            RuntimeError: if an unsupported request is made.
        """
        request_bridge = self.request_bridge
        report_generator = self.system.report_generator
        random_search = self.system.random_search

        # used to keep track if there is new completed work to display
        work_was_in_progress = False
        while True:
            work_in_progress = self.send_progress_update()

            completed_work = not work_in_progress and work_was_in_progress
            work_was_in_progress = work_in_progress
            if completed_work:
                self.send_current_state()

            message = None
            if work_in_progress:
                message = request_bridge.get_request()
            else:
                message = request_bridge.get_request_blocking()

            match message:
                case None:
                    continue
                case ReportRequestMessage(request=HyperParameterRequest.end):
                    self.system.shutdown()
                    break
                case ReportRequestMessage(
                    request=HyperParameterRequest.generate_report,
                    payload=parameter,
                ):
                    report_generator.generate_report(parameter)
                    self.send_current_state()
                case ReportRequestMessage(
                    request=HyperParameterRequest.fetch_current_state
                ):
                    self.send_current_state()
                case ReportRequestMessage(
                    request=HyperParameterRequest.set_searching_state,
                    payload=True,
                ):
                    random_search.start_search()
                case ReportRequestMessage(
                    request=HyperParameterRequest.set_searching_state,
                    payload=False,
                ):
                    random_search.stop_search()
                case _:
                    raise RuntimeError("Unsupported report request.")

    def send_progress_update(self) -> bool:
        """Send progress updates to the user if they are warranted.

        A progress update is required when it has been long enough from the last
        one and there is some work in progress.

        Returns:
            bool: weather there is work in progress
        """
        state = self.system.get_state()

        report_in_progress = bool(state.report.pending_requests)
        search_in_progress = state.search.searching

        work_in_progress = report_in_progress or search_in_progress

        next_update = (
            self.last_update_timestamp + self.minimum_update_delta_seconds
        )

        if time() < next_update:
            return work_in_progress

        if work_in_progress:
            # send progress update
            self.send_current_state()

        return work_in_progress

    def send_current_state(self):
        """Send the current state to the view."""
        self.last_update_timestamp = time()
        current_state = self.system.get_state()
        self.update_bridge.update_state(current_state)
