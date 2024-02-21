from typing import Optional, Union

from PySide6.QtCore import Qt
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
    potential_reward_text = "Potential Reward"
    regret = "Regret"
    missing_value_text = "—"

    top_title = "Configuration"
    middle_title = "Statistics"
    parameters_title = "Best Hyperparameter Values"

    def __init__(
        self,
        parent: Optional[QWidget],
        search_state: RandomSearchState,
        search_area: SearchArea,
    ) -> None:
        """Initialise the display.

        Args:
            parent (Optional[QWidget]): the parent of this widget.
            search_state (RandomSearchState): the search state information.
            search_area (SearchArea): the search area to display.
        """
        super().__init__(parent)

        self.setFrameShape(self.Shape.Box)
        self.layout_manager = QGridLayout(self)
        self.row: int = 0

        potential_reward = None
        if search_state.optimal_rewards is not None:
            potential_reward = search_state.optimal_rewards[
                search_area.options.dynamics
            ]

        self.__populate_config(search_area)
        self.__populate_stats(search_area, potential_reward)
        self.__populate_parameters(search_area)

    def __populate_config(self, search_area: SearchArea):
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

    def __populate_stats(
        self, search_area: SearchArea, potential_reward: Optional[float]
    ):
        self.__add_title(self.middle_title)
        self.__add_row(self.best_value_text, search_area.best_value)
        self.__add_row(self.potential_reward_text, potential_reward)

        if potential_reward is None or search_area.best_value is None:
            self.__add_row(self.regret, None)
        else:
            self.__add_row(
                self.regret, potential_reward - search_area.best_value
            )

        self.__add_row(self.total_attempts_text, search_area.combinations_tried)

    def __populate_parameters(self, search_area: SearchArea):
        self.__add_title(self.parameters_title)
        best_parameters = search_area.best_parameters

        for parameter, parameter_value in best_parameters.items():
            details = TuningInformation.get_parameter_details(parameter)

            self.__add_row(
                details.name, parameter_value, details.integer_valued
            )

    def __add_title(self, title: str):
        title_label = QLabel(title, self)

        current_font = title_label.font()
        current_font.setBold(True)
        current_font.setPointSize(current_font.pointSize() + 2)
        title_label.setFont(current_font)
        self.layout_manager.addWidget(title_label, self.row, 0, 1, 2)
        self.row += 1

    def __add_row(
        self,
        label: str,
        row_data: Union[float, int, str, None],
        display_as_int: bool = False,
    ):
        self.layout_manager.addWidget(
            QLabel(label, self),
            self.row,
            0,
        )
        text = None

        if row_data is None:
            text = self.missing_value_text
        elif isinstance(row_data, int) or display_as_int:
            text = f"{row_data: d}"
        elif isinstance(row_data, float):
            text = f"{row_data: .3f}"
        else:
            text = row_data

        alignment = (
            Qt.AlignmentFlag.AlignCenter
            if row_data is None
            else Qt.AlignmentFlag.AlignLeft
        )
        data_label = self.__add_selection(QLabel(text, self))

        self.layout_manager.addWidget(data_label, self.row, 1, alignment)
        self.row += 1

    def __add_selection(self, label: QLabel) -> QLabel:
        flags = (
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        label.setTextInteractionFlags(flags)
        return label


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
            section = SearchDisplaySection(self, search_state, search_area)
            layout.addWidget(section, index // columns, index % columns)
