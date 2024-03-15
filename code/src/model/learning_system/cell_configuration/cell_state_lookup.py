from typing import Dict, Optional, Tuple

from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.state.state_instance import StateInstance, entities_type

lookup_table_type = Dict[Tuple[int, int, entities_type], StateInstance]


class CellStateLookup(object):
    """This class represents lookup tables for mapping cells to states."""

    def __init__(self, dynamics: BaseDynamics) -> None:
        """Initialise the class.

        Args:
            dynamics (BaseDynamics): the dynamics this lookup is based upon.
        """
        self.dynamics = dynamics
        self.cell_lookup_table: Optional[lookup_table_type] = None

    def get_state(
        self, reference_state: StateInstance, cell: Tuple[int, int]
    ) -> Optional[StateInstance]:
        """Get a state with an agent in a given cell based on the reference.

        Args:
            reference_state (StateInstance): the base state to compare with
            cell (Tuple[int, int]): the cell the agent should be in.

        Returns:
            Optional[StateInstance]: returns the relevant state if one exists.
        """
        if self.cell_lookup_table is None:
            self.cell_lookup_table = self.build_lookup_table()

        cell_x, cell_y = cell
        key = (cell_x, cell_y, reference_state.entities)
        return self.cell_lookup_table.get(key, None)

    def build_lookup_table(self) -> lookup_table_type:
        """Populate the lookup table.

        Returns:
            lookup_table_type: the populated lookup table.
        """
        self.cell_lookup_table = {}
        for state in self.dynamics.state_pool.id_to_state.values():
            location_x, location_y = state.agent_location
            key = (location_x, location_y, state.entities)
            existing = self.cell_lookup_table.get(key, None)
            if existing is None:
                self.cell_lookup_table[key] = state

        return self.cell_lookup_table
