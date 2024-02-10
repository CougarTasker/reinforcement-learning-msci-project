from dataclasses import dataclass
from typing import Tuple

from immutables import Map
from typing_extensions import Self

from .cell_entities import CellEntity

entities_type = Map[tuple[int, int], CellEntity]


@dataclass(frozen=True, slots=True)
class StateInstance(object):
    """This class represents a possible state in the grid world of this MDP."""

    agent_location: Tuple[int, int]
    entities: entities_type

    @classmethod
    def get_blank_state(cls) -> Self:
        """Create a blank state.

        Returns:
            Self: a state with no particular features.
        """
        return cls((0, 0), Map())
