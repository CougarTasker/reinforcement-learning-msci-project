from dataclasses import dataclass
from typing import Dict, List

from src.model.hyperparameters.base_parameter_strategy import HyperParameter


@dataclass(frozen=True, slots=True)
class HyperParameterReport(object):
    """Describes the effect of a hyper parameter."""

    parameter: HyperParameter
    x_axis: List
    y_axis: List


@dataclass(frozen=True, slots=True)
class ReportState(object):
    """Contains the state of all the reports."""

    pending_requests: set[HyperParameter]
    available_reports: Dict[HyperParameter, HyperParameterReport]

    def add_pending_request(self, request: HyperParameter) -> "ReportState":
        """Get the new state after a new request is made.

        Args:
            request (HyperParameter): the report the user wants generated.

        Returns:
            ReportState: the current state of all reports
        """
        if request in self.pending_requests:
            return self
        if request in self.available_reports:
            return self

        pending_requests = self.pending_requests.copy()
        pending_requests.add(request)
        return ReportState(pending_requests, self.available_reports)

    def complete_request(self, report: HyperParameterReport) -> "ReportState":
        """Create the new state after a report is completed.

        Args:
            report (HyperParameterReport): The new completed report.

        Returns:
            ReportState: the new report state including the new report
        """
        parameter = report.parameter
        pending_requests = self.pending_requests.copy()
        pending_requests.remove(parameter)
        available_reports = self.available_reports.copy()
        available_reports[parameter] = report
        return ReportState(pending_requests, available_reports)
