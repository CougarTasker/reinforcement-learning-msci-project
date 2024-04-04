from dataclasses import dataclass
from enum import Enum

from src.model.learning_system.cell_configuration.cell_configuration import (
    DisplayMode,
)
from src.model.learning_system.top_level_entities.options import (
    TopEntitiesOptions,
)


class AutomaticOptions(Enum):
    """Enumerates the possible automatic states."""

    manual = 0
    automatic_paused = 1
    automatic_playing = 2


@dataclass(frozen=True, slots=True)
class GlobalOptions(object):
    """Class represents the current options."""

    top_level_options: TopEntitiesOptions
    display_mode: DisplayMode
    automatic: AutomaticOptions
