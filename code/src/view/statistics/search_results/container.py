from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QScrollArea, QWidget
from typing_extensions import override

from src.controller.hyper_parameter_controller.controller import (
    HyperParameterController,
)
from src.model.hyperparameters.hyper_parameter_system import HyperParameterState
from src.model.hyperparameters.random_search.random_search_data import (
    RandomSearchState,
)
from src.view.report_state_publisher import (
    BaseReportObserver,
    ReportStatePublisher,
)
from src.view.statistics.search_results.display import SearchDisplayInstance
from src.view.statistics.search_results.start_button import SearchStartButton


class SearchDisplay(QWidget, BaseReportObserver):
    """Display the results of the ongoing random search.

    This class contains the controls to update the search and the updated
    details.
    """

    def __init__(
        self,
        parent: Optional[QWidget],
        report_controller: HyperParameterController,
        publisher: ReportStatePublisher,
    ) -> None:
        """Initialise the search display.

        Args:
            parent (Optional[QWidget]): the parent this widget is mounted in.
            report_controller (HyperParameterController): the controller to
                interact with.
            publisher (ReportStatePublisher): the publisher to notify the
                display of updates.
        """
        super().__init__(parent)
        layout = QGridLayout(self)

        button = SearchStartButton(self, report_controller)
        publisher.subscribe(button)
        layout.addWidget(button, 0, 0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scroll_area, 1, 0)

        publisher.subscribe(self)

        self.lest_search_state: Optional[RandomSearchState] = None

    @override
    def report_state_updated(self, state: HyperParameterState) -> None:
        """Update the details view with new information.

        Args:
            state (HyperParameterState): The current state.
        """
        search_state = state.search
        if search_state == self.lest_search_state:
            return
        self.lest_search_state = search_state
        # save scroll position
        v_scrollbar = self.scroll_area.verticalScrollBar()
        h_scrollbar = self.scroll_area.horizontalScrollBar()
        v_pos = v_scrollbar.sliderPosition()
        h_pos = h_scrollbar.sliderPosition()
        # scroll position lost
        self.scroll_area.setWidget(
            SearchDisplayInstance(self.scroll_area, search_state),
        )
        # restore scroll position
        v_scrollbar.setSliderPosition(v_pos)
        h_scrollbar.setSliderPosition(h_pos)
