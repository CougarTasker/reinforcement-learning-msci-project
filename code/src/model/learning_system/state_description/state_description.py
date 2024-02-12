from dataclasses import dataclass
from typing import Dict

from src.model.dynamics.grid_world import GridWorld, integer_position
from src.model.learning_system.cell_configuration.cell_configuration import (
    CellConfiguration,
)
from src.model.learning_system.global_options import GlobalOptions
from src.model.state.state_instance import StateInstance

from ..learning_instance.statistics_record import StatisticsRecord

cell_config_listing = Dict[integer_position, CellConfiguration]


@dataclass
class StateDescription(object):
    """Compile together the dynamic and static state information.

    Provides all of the state information in a picklable object for the view.
    """

    grid_world: GridWorld
    state: StateInstance
    cell_config: cell_config_listing
    global_options: GlobalOptions
    statistics: StatisticsRecord
