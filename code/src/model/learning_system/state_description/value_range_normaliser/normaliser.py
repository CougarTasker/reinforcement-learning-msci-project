from typing import Dict, Tuple, Union

from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.actions import Action
from src.model.state.state_instance import StateInstance
from src.model.state.state_pool import StatePool

from ..value_range_normaliser.value_range import ValueRange, ValueType

action_value_tuple = Tuple[StateInstance, Action]


class StateValueNormaliser(object):
    """Compute the normalised value of an agent being in a state."""

    def __init__(
        self,
        agent: BaseAgent,
        state_pool: StatePool,
        value_range: ValueRange,
    ) -> None:
        """Initialise the normaliser.

        this class will normalise the values between 0 and 1.


        Args:
            agent (BaseAgent): the agent to decide the value
            state_pool (StatePool): a state pool with all possible states.
            entities (entities_type): the entity space to consider.
            value_range (ValueRange): the range of possible values for this
                agent and dynamics
        """
        self.agent = agent
        self.state_pool = state_pool
        self.value_range = value_range
        self.state_value_cache: Dict[StateInstance, float] = {}
        self.action_value_cache: Dict[action_value_tuple, float] = {}

    def get_state_action_value_normalised(
        self,
        state: StateInstance,
        action: Action,
    ) -> Union[float, None]:
        """Get the normalised value of a given agent location and action.

        Args:
            new_agent_location (Tuple[int, int]): the new agents location
            action (Action): the action to perform

        Returns:
            Union[float, None]: the value if one can be found.
        """
        cache_key = (state, action)
        cached_value = self.action_value_cache.get(cache_key, None)
        if cached_value is not None:
            return cached_value

        action_value = self.value_range.rescale_value(
            ValueType.state_action_value,
            self.agent.get_state_action_value(
                self.state_pool.get_state_id(state), action
            ),
        )
        self.action_value_cache[cache_key] = action_value
        return action_value

    def get_state_value_normalised(
        self, state: StateInstance
    ) -> Union[float, None]:
        """Get the normalised value of the agent being in this location.

        Args:
            new_agent_location (Tuple[int, int]): the new agents location

        Returns:
            Union[float, None]: the value if one can be found.
        """
        cached_value = self.state_value_cache.get(state, None)
        if cached_value is not None:
            return cached_value

        state_value = self.value_range.rescale_value(
            ValueType.state_value,
            self.agent.get_state_value(self.state_pool.get_state_id(state)),
        )
        self.state_value_cache[state] = state_value

        return state_value
