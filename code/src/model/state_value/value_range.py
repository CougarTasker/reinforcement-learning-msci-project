from enum import Enum
from typing import Optional, Tuple

from ..agents.base_agent import BaseAgent
from ..dynamics.actions import Action
from ..state.state_pool import StatePool


class ValueType(Enum):
    """Enumerates the possible types of values."""

    state_value = 0
    state_action_value = 1


class ValueRange(object):
    """Maintains the range of all possible values for mapping from 0 to 1."""

    def __init__(self, state_pool: StatePool, agent: BaseAgent) -> None:
        """Initialise a value range.

        Args:
            state_pool (StatePool): the populated set of all possible states to
            find the range of values.
            agent (BaseAgent): the agent to decide on values
        """
        self.state_pool = state_pool
        self.agent = agent

        self.action_range: Optional[Tuple[float, float]] = None

        self.state_range: Optional[Tuple[float, float]] = None

    def rescale_value(
        self, value_type: ValueType, absolute_value: float
    ) -> float:
        """Rescale a value from a value type into the range 0-1.

        the minimum value of this type would get a value of 0 and the maximum
        value of this type would get a 1.

        Args:
            value_type (ValueType): the type of value received
            absolute_value (float): the raw value before rescaling

        Returns:
            float: _description_
        """
        min_value, max_value = self.__get_value_range(value_type)
        return (absolute_value - min_value) / (max_value - min_value)

    def __get_value_range(self, value_type: ValueType) -> Tuple[float, float]:
        match value_type:
            case ValueType.state_value:
                return self.__get_state_value_range()
            case ValueType.state_action_value:
                return self.__get_state_action_value_range()

    def __get_state_value_range(self) -> Tuple[float, float]:
        if self.state_range is not None:
            return self.state_range
        maximum_state_value = float("-inf")
        minimum_state_value = float("inf")
        for state in self.state_pool.state_to_id.values():
            state_value = self.agent.get_state_value(state)
            maximum_state_value = max(maximum_state_value, state_value)
            minimum_state_value = min(minimum_state_value, state_value)

        self.state_range = (minimum_state_value, maximum_state_value)
        return self.state_range

    def __get_state_action_value_range(self) -> Tuple[float, float]:
        if self.action_range is not None:
            return self.action_range

        maximum_action_value = float("-inf")
        minimum_action_value = float("inf")

        for state in self.state_pool.state_to_id.values():
            for action in Action:
                action_value = self.agent.get_state_action_value(state, action)
                maximum_action_value = max(maximum_action_value, action_value)
                minimum_action_value = min(minimum_action_value, action_value)

        self.action_range = (minimum_action_value, maximum_action_value)
        return self.action_range
