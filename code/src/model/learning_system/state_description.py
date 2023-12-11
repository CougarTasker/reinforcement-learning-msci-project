from typing import Dict

from src.model.dynamics.grid_world import GridWorld, integer_position
from src.model.state.state_instance import StateInstance

from .cell_configuration import CellConfiguration, DisplayMode

cell_config_listing = Dict[integer_position, CellConfiguration]


class StateDescription(object):
    """Compile together the dynamic static state information."""

    def __init__(
        self,
        grid_world: GridWorld,
        state: StateInstance,
        cell_config: cell_config_listing,
        display_mode: DisplayMode,
    ) -> None:
        """Initiate this state description.

        Args:
            grid_world (GridWorld): the grid world of this state.
            state (StateInstance): the state to describe.
            cell_config (cell_config_listing): the configuration for cells in
                the view. allowing for visualisations of the current state
                value table.
            display_mode (DisplayMode): how to display this state.
        """
        self.grid_world = grid_world
        self.state = state
        self.display_mode = display_mode
        self.cell_config = cell_config
