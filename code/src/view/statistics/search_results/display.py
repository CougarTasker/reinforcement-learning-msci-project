from typing import Optional

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QWidget

from src.model.hyperparameters.random_search.random_search_data import (
    RandomSearchState,
    SearchArea,
)
from src.model.hyperparameters.tuning_information import TuningInformation
from src.view.option_display_text import OptionDisplayText


class SearchDisplaySection(QFrame):
    """Display the results of a random search."""

    dynamics_used_text = "Dynamics"
    exploration_strategy_text = "Exploration Strategy"

    best_value_text = "Best Total Reward"
    total_attempts_text = "Total Attempts"
    missing_value_text = "-"

    top_title = "Configuration"
    middle_title = "Statistics"
    parameters_title = "Best Hyperparameter Values"

    def __init__(
        self,
        parent: Optional[QWidget],
        search_area: SearchArea,
    ) -> None:
        """Initialise the display.

        Args:
            parent (Optional[QWidget]): the parent of this widget.
            search_area (SearchArea): the search area to display.
        """
        super().__init__(parent)

        self.setFrameShape(self.Shape.Box)
        self.layout_manager = QGridLayout(self)
        self.row: int = 0
        self.__populate_rows(search_area)

    def __populate_rows(self, search_area: SearchArea):
        options = search_area.options

        self.__add_title(self.top_title)

        self.__add_row(
            self.exploration_strategy_text,
            OptionDisplayText.full_exploration_options.get_text(
                options.exploration_strategy
            ),
        )

        self.__add_row(
            self.dynamics_used_text,
            OptionDisplayText.dynamics_options.get_text(options.dynamics),
        )
        self.__add_title(self.middle_title)

        best_value = (
            self.missing_value_text
            if search_area.best_value is None
            else f"{search_area.best_value:.3f}"
        )

        self.__add_row(self.best_value_text, best_value)

        self.__add_row(
            self.total_attempts_text, str(search_area.combinations_tried)
        )
        self.__add_title(self.parameters_title)
        best_parameters = search_area.best_parameters

        for parameter, parameter_value in best_parameters.items():
            details = TuningInformation.get_parameter_details(parameter)

            if parameter_value is None:
                self.__add_row(details.name, self.missing_value_text)
                continue

            text_value = (
                f"{parameter_value:d}"
                if details.integer_valued
                else f"{parameter_value:.3f}"
            )
            self.__add_row(details.name, text_value)

    def __add_title(self, title: str):
        title_label = QLabel(title, self)

        current_font = title_label.font()
        current_font.setBold(True)
        current_font.setPointSize(current_font.pointSize() + 1)
        title_label.setFont(current_font)
        self.layout_manager.addWidget(title_label, self.row, 0, 1, 2)
        self.row += 1

    def __add_row(self, label: str, text: str):
        self.layout_manager.addWidget(
            QLabel(label, self),
            self.row,
            0,
        )
        self.layout_manager.addWidget(
            QLabel(text, self),
            self.row,
            1,
        )
        self.row += 1


class SearchDisplayInstance(QWidget):
    """Display the results of a random search."""

    dynamics_used_text = "Dynamics"
    exploration_strategy_text = "Exploration Strategy"

    best_value_text = "Best Total Reward"
    total_attempts_text = "Total Attempts"

    def __init__(
        self, parent: Optional[QWidget], search_state: RandomSearchState
    ) -> None:
        """Initialise the display.

        Args:
            parent (Optional[QWidget]): the parent of this widget.
            search_state (RandomSearchState): the state to display.
        """
        super().__init__(parent)
        layout = QGridLayout(self)

        columns = 2

        for index, search_area in enumerate(search_state.search_areas.values()):
            section = SearchDisplaySection(self, search_area)
            layout.addWidget(section, index // columns, index % columns)
