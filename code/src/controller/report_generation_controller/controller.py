from multiprocessing import Process
from typing import Optional

from typing_extensions import Self

from src.controller.report_generation_controller.report_request_bridge import (
    ReportRequest,
    ReportRequestBridge,
    ReportRequestMessage,
)
from src.controller.report_generation_controller.report_update_bridge import (
    ReportUpdateBridge,
)
from src.model.hyperparameters.report_generator import (
    HyperParameterReportGenerator,
)


class ReportGeneratorController(object):
    """Controller for managing the report generator."""

    def __init__(self) -> None:
        """Initialise the learning system controller."""
        self.report_generator = HyperParameterReportGenerator()

        self.report_request_bridge = ReportRequestBridge()
        self.report_update_bridge = ReportUpdateBridge()

        self.report_process: Optional[Process] = None

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
        self.report_request_bridge.request_shutdown()
        if self.report_process is not None:
            self.report_process.join()

    def report_mainloop(
        self,
    ):
        """Run the main loop of the report generation process.

        Raises:
            RuntimeError: if an unsupported request is made.
        """
        request_bridge = self.report_request_bridge
        report_generator = self.report_generator

        report_count = 0  # number of generated reports
        while True:
            current_state = report_generator.get_state()

            new_report_count = len(current_state.available_reports)
            if new_report_count > report_count:
                self.send_current_state()
                report_count = new_report_count

            message = None
            if current_state.pending_requests:
                message = request_bridge.get_request()
            else:
                message = request_bridge.get_request_blocking()

            match message:
                case None:
                    continue
                case ReportRequestMessage(request=ReportRequest.end):
                    break
                case ReportRequestMessage(
                    request=ReportRequest.generate_report, payload=parameter
                ):
                    report_generator.generate_report(parameter)

                case ReportRequestMessage(
                    request=ReportRequest.fetch_current_state
                ):
                    self.send_current_state()
                case _:
                    raise RuntimeError("Unsupported report request.")

    def send_current_state(self):
        """Send the current state to the view."""
        current_state = self.report_generator.get_state()
        self.report_update_bridge.update_report_state(current_state)
