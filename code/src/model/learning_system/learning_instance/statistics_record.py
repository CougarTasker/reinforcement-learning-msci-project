from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class StatisticsRecord(object):
    """Class to contain a record of the statistics."""

    time_step: int
    reward_history: List[float]
    total_reward: float
    current_state: Optional[int] = None
