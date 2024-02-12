from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from src.model.hyperparameters.base_parameter_strategy import HyperParameter

from ..base_bridge import BaseBridge


class ReportRequest(Enum):
    """Enumerate all possible user actions."""

    end = 0
    generate_report = 1


@dataclass(frozen=True, slots=True)
class ReportRequestMessage(object):
    """Encapsulates a user action and its data."""

    request: ReportRequest
    payload: Any = None


class ReportRequestBridge(BaseBridge):
    """Bridge for passing the report requests from the view to the model."""

    def request_shutdown(self) -> None:
        """Request to shutdown the report generator."""
        self.add_item(ReportRequestMessage(ReportRequest.end))

    def request_report(self, parameter: HyperParameter) -> None:
        """Request report from the generator.

        Args:
            parameter (HyperParameter): the hyper-parameter to generate a
                report for.
        """
        self.add_item(
            ReportRequestMessage(ReportRequest.generate_report, parameter)
        )

    def get_request(self) -> Optional[ReportRequestMessage]:
        """Get the latest requested report if there is one.

        Returns:
            Optional[ReportRequestMessage]: the latest request, None if no
                request has been made.
        """
        return self.get_item_non_blocking()

    def get_request_blocking(self) -> ReportRequestMessage:
        """Get the latest request, block until a request is made.

        can be used while there is no pending requests to avoid computation.

        Returns:
            ReportRequestMessage: the latest request.
        """
        return self.get_item_blocking()
