from dataclasses import dataclass

from src.model.hyperparameters.random_search.random_search import RandomSearch
from src.model.hyperparameters.random_search.random_search_data import (
    RandomSearchState,
)
from src.model.hyperparameters.report_generation.report_data import ReportState
from src.model.hyperparameters.report_generation.report_generator import (
    HyperParameterReportGenerator,
)


@dataclass(frozen=True, slots=True)
class HyperParameterState(object):
    """State object for combining all hyper parameter state."""

    report: ReportState
    search: RandomSearchState


class HyperParameterSystem(object):
    """class for combining hyper parameter functionality."""

    def __init__(self) -> None:
        """Initialise the hyper parameter system."""
        self.report_generator = HyperParameterReportGenerator()
        self.random_search = RandomSearch()

    def get_state(self) -> HyperParameterState:
        """Get the combined hyper parameter state.

        Returns:
            HyperParameterState: the state of the hyper parameter systems
        """
        report = self.report_generator.get_state()
        search = self.random_search.get_progress()
        return HyperParameterState(report, search)

    def shutdown(self):
        """Stop any ongoing work."""
        self.report_generator.shutdown()
        self.random_search.stop_search()
