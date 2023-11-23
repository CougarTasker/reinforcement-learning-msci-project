from ..model.dynamics.base_dynamics import BaseDynamics
from ..model.state.cell_entities import CellEntity
from ..model.state_value.normaliser import StateValueNormaliser


class StateDescription(object):
    """Compile together the dynamic static state information."""

    def __init__(
        self,
        dynamics: BaseDynamics,
        state: int,
        normaliser: StateValueNormaliser,
    ) -> None:
        """Initiate this state description.

        Args:
            dynamics (BaseDynamics): the dynamics this state is a part of
            state (int): the state to describe
            normaliser (StateValueNormaliser): the state value normaliser
            allowing for visualisations of the current state value table.
        """
        self.grid_world = dynamics.grid_world
        self.state = dynamics.state_pool.get_state_from_id(state)
        self.normaliser = normaliser

    def cell_entity(self, cell: tuple[int, int]) -> CellEntity:
        """Get the cell entity at a given location.

        Args:
            cell (tuple[int, int]): the location of the cell to check.

        Raises:
            ValueError: if the cell is not a valid location

        Returns:
            CellEntity: the cell entity at this location
        """
        if not self.grid_world.is_in_bounds(cell):
            raise ValueError(f"location {cell} is not in bounds")

        if cell == self.state.agent_location:
            return CellEntity.agent

        return self.state.entities.get(cell, CellEntity.empty)
