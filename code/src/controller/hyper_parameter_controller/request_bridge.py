from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from src.model.hyperparameters.base_parameter_strategy import HyperParameter

from ..base_bridge import BaseBridge


class HyperParameterRequest(Enum):
    """Enumerate all possible user actions."""

    end = 0
    generate_report = 1
    fetch_current_state = 2
    set_searching_state = 3


@dataclass(frozen=True, slots=True)
class ReportRequestMessage(object):
    """Encapsulates a user action and its data."""

    request: HyperParameterRequest
    payload: Any = None


class HyperParameterRequestBridge(BaseBridge):
    """Bridge for passing the report requests from the view to the model."""

    def request_current_state(self) -> None:
        """Request to receive the current state."""
        self.add_item(
            ReportRequestMessage(HyperParameterRequest.fetch_current_state)
        )

    def request_shutdown(self) -> None:
        """Request to shutdown the report generator."""
        self.add_item(ReportRequestMessage(HyperParameterRequest.end))

    def request_report(self, parameter: HyperParameter) -> None:
        """Request report from the generator.

        Args:
            parameter (HyperParameter): the hyper-parameter to generate a
                report for.
        """
        self.add_item(
            ReportRequestMessage(
                HyperParameterRequest.generate_report, parameter
            )
        )

    def set_search_state(self, running: bool) -> None:
        """Request to set the searching state.

        Args:
            running (bool): the new search state.
        """
        self.add_item(
            ReportRequestMessage(
                HyperParameterRequest.set_searching_state, running
            )
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
