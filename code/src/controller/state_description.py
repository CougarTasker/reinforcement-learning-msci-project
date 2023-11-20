from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.state.cell_entities import CellEntity


class StateDescription(object):
    """Compile together the dynamic static state information."""

    def __init__(self, dynamics: BaseDynamics, state: int) -> None:
        """Initiate this state description.

        Args:
            dynamics (BaseDynamics): the dynamics this state is a part of
            state (int): the state to describe
        """
        self.grid_world = dynamics.grid_world
        self.state = dynamics.state_pool.get_state_from_id(state)

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
