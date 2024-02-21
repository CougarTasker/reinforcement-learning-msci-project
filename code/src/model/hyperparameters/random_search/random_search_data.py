from dataclasses import dataclass, replace
from typing import Dict, Optional

from src.model.hyperparameters.base_parameter_strategy import HyperParameter
from src.model.hyperparameters.random_search.random_parameter_strategy import (
    RandomParameterStrategy,
)
from src.model.learning_system.top_level_entities.options import (
    DynamicsOptions,
    TopEntitiesOptions,
)


@dataclass(frozen=True, slots=True)
class SearchArea(object):
    """Represents the results of a search in a particular area."""

    options: TopEntitiesOptions
    best_parameters: Dict[HyperParameter, Optional[float]]
    best_value: Optional[float]
    combinations_tried: int

    def record_result(
        self, hyper_parameters: RandomParameterStrategy, recorded_value: float
    ) -> "SearchArea":
        """Get the new search area state after recording a new value.

        Args:
            hyper_parameters (RandomParameterStrategy): the parameters that
                were tested.
            recorded_value (float): the value recorded by these parameters.

        Returns:
            SearchArea: the new search area with these changes.
        """
        combinations_tried = self.combinations_tried + 1

        if self.best_value is None or recorded_value > self.best_value:
            return SearchArea(
                self.options,
                hyper_parameters.get_parameters(),
                recorded_value,
                combinations_tried,
            )

        return SearchArea(
            self.options,
            self.best_parameters,
            self.best_value,
            combinations_tried,
        )


@dataclass(frozen=True, slots=True)
class RandomSearchState(object):
    """Class to contain the state of a random search."""

    optimal_rewards: Optional[Dict[DynamicsOptions, float]]
    search_areas: Dict[TopEntitiesOptions, SearchArea]
    searching: bool

    def record_result(
        self,
        options: TopEntitiesOptions,
        hyper_parameters: RandomParameterStrategy,
        recorded_value: float,
    ) -> "RandomSearchState":
        """Get the new search area state after recording a new value.

        Args:
            options (TopEntitiesOptions): the options used for this record.
            hyper_parameters (RandomParameterStrategy): the parameters that
                were tested.
            recorded_value (float): the value recorded by these parameters.

        Returns:
            RandomSearchData: the new state after this result.
        """
        search_areas = self.search_areas.copy()
        new_search_area = search_areas[options].record_result(
            hyper_parameters, recorded_value
        )
        search_areas[options] = new_search_area
        return replace(self, search_areas=search_areas)

    def set_searching(self, searching: bool) -> "RandomSearchState":
        """Set the searching property.

        Args:
            searching (bool): Weather the search process is ongoing.

        Returns:
            RandomSearchState: The new state with the updated value.
        """
        return replace(self, searching=searching)

    def set_optimal_rewards(
        self, optimal_rewards: Dict[DynamicsOptions, float]
    ) -> "RandomSearchState":
        """Set the optimal reward for a given dynamics.

        sets a listing of the best reward possible for each dynamics.

        Args:
            optimal_rewards (Dict[DynamicsOptions, float]): the best reward
                possible.

        Returns:
            RandomSearchState: the state that includes this information.
        """
        return replace(self, optimal_rewards=optimal_rewards)
