from dataclasses import dataclass, replace
from typing import Dict, List, Optional

from src.model.hyperparameters.base_parameter_strategy import HyperParameter


@dataclass(frozen=True, slots=True)
class HyperParameterReport(object):
    """Describes the effect of a hyper parameter."""

    parameter: HyperParameter
    x_axis: List
    y_axis: List


incomplete_progress_cap = 0.99


@dataclass(frozen=True, slots=True)
class ReportState(object):
    """Contains the state of all the reports."""

    current_report: Optional[HyperParameter]
    pending_requests: Dict[HyperParameter, float]

    available_reports: Dict[HyperParameter, HyperParameterReport]

    def report_requested(self, request: HyperParameter) -> "ReportState":
        """Get the new state after a new request is made.

        Args:
            request (HyperParameter): the report the user wants generated.

        Returns:
            ReportState: the current state of all reports
        """
        pending = request in self.pending_requests
        available = request in self.available_reports
        if pending or available:
            if request is self.current_report:
                return self
            return replace(self, current_report=request)

        pending_requests = self.pending_requests.copy()
        pending_requests[request] = 0
        return ReportState(request, pending_requests, self.available_reports)

    def update_report_progress(
        self, parameter: HyperParameter, progress: float
    ) -> "ReportState":
        """Update the progress marker for a pending report.

        Args:
            parameter (HyperParameter): the pending report
            progress (float): the new progress of this report

        Returns:
            ReportState: the new state with the updated progress.
        """
        if parameter not in self.pending_requests:
            return self

        pending_requests = self.pending_requests.copy()
        # if progress of an incomplete report is >= 1 it can break
        # a progress assumption made by the controller
        pending_requests[parameter] = min(progress, incomplete_progress_cap)
        return ReportState(
            self.current_report, pending_requests, self.available_reports
        )

    def complete_request(self, report: HyperParameterReport) -> "ReportState":
        """Create the new state after a report is completed.

        Args:
            report (HyperParameterReport): The new completed report.

        Returns:
            ReportState: the new report state including the new report
        """
        parameter = report.parameter
        pending_requests = self.pending_requests.copy()
        pending_requests.pop(parameter)
        available_reports = self.available_reports.copy()
        available_reports[parameter] = report
        return ReportState(
            self.current_report, pending_requests, available_reports
        )
