"""This package contains the agents.

the agents should that will learn and generate policies
"""


# import agents to simplify imports later
from .base_agent import BaseAgent  # Noqa: F401
from .q_learning.agent import QLearningAgent  # Noqa: F401
from .value_iteration.agent import ValueIterationAgent  # Noqa: F401
from .value_iteration.agent_optimised import (  # Noqa: F401
    ValueIterationAgentOptimised,
)
