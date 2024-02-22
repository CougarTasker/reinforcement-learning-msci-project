from enum import Enum


class ExplorationStrategyOptions(Enum):
    """Enumerates all exploration strategies."""

    not_applicable = 0
    epsilon_greedy = 1
    upper_confidence_bound = 2
    mf_bpi = 3
