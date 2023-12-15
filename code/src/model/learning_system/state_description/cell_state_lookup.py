from typing import Dict, Optional, Tuple

from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.state.state_instance import StateInstance, entities_type


class CellStateLookup(object):
    def __init__(self, dynamics: BaseDynamics) -> None:
        self.dynamics = dynamics
        self.cell_lookup_table: Optional[
            Dict[Tuple[int, int, entities_type], StateInstance]
        ] = None

    def get_state(
        self, reference_state: StateInstance, cell: Tuple[int, int]
    ) -> Optional[StateInstance]:
        if self.cell_lookup_table is None:
            self.cell_lookup_table = self.build_lookup_table()

        x, y = cell
        key = (x, y, reference_state.entities)
        return self.cell_lookup_table.get(key, None)

    def build_lookup_table(self):
        self.cell_lookup_table = {}
        for state in self.dynamics.state_pool.id_to_state.values():
            x, y = state.agent_location
            key = (x, y, state.entities)
            existing = self.cell_lookup_table.get(key, None)
            if existing is None or existing.agent_energy < state.agent_energy:
                self.cell_lookup_table[key] = state

        return self.cell_lookup_table
