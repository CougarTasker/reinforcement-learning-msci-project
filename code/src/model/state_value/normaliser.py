from typing import Dict, Optional, Tuple, Union

from src.model.state_value.value_range import ValueRange, ValueType

from ..agents.base_agent import BaseAgent
from ..dynamics.actions import Action
from ..state.state_instance import entities_type
from ..state.state_pool import StatePool

action_value_tuple = Tuple[Tuple[int, int], Action]


class StateValueNormaliser(object):
    """Compute the normalised value of an agent being in a state."""

    def __init__(
        self,
        agent: BaseAgent,
        state_pool: StatePool,
        entities: entities_type,
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
        self.entities = entities
        self.value_range = value_range
        self.state_value_cache: Dict[Tuple[int, int], float] = {}
        self.action_value_cache: Dict[action_value_tuple, float] = {}

    def get_state_action_value_normalised(
        self,
        new_agent_location: Tuple[int, int],
        action: Action,
    ) -> Union[float, None]:
        """Get the normalised value of a given agent location and action.

        Args:
            new_agent_location (Tuple[int, int]): the new agents location
            action (Action): the action to perform

        Returns:
            Union[float, None]: the value if one can be found.
        """
        cache_key = (new_agent_location, action)
        cached_value = self.action_value_cache.get(cache_key, None)
        if cached_value is not None:
            return cached_value

        state = self.__get_agent_state(new_agent_location)
        if state is None:
            return None
        action_value = self.value_range.rescale_value(
            ValueType.state_action_value,
            self.agent.get_state_action_value(state, action),
        )
        self.action_value_cache[cache_key] = action_value
        return action_value

    def get_state_value_normalised(
        self, new_agent_location: Tuple[int, int]
    ) -> Union[float, None]:
        """Get the normalised value of the agent being in this location.

        Args:
            new_agent_location (Tuple[int, int]): the new agents location

        Returns:
            Union[float, None]: the value if one can be found.
        """
        cached_value = self.state_value_cache.get(new_agent_location, None)
        if cached_value is not None:
            return cached_value

        state = self.__get_agent_state(new_agent_location)
        if state is None:
            return None

        state_value = self.value_range.rescale_value(
            ValueType.state_value,
            self.agent.get_state_value(state),
        )
        self.state_value_cache[new_agent_location] = state_value

        return state_value

    def get_state_action_value_raw(
        self, new_agent_location: Tuple[int, int], action: Action
    ) -> Optional[float]:
        """Get the un-normalised value of a given agent location and action.

        Args:
            new_agent_location (Tuple[int, int]): the location the agent is in
            action (Action): the action to perform.

        Returns:
            Optional[float]: the raw value of this action state combination
            according to the agent.
        """
        state = self.__get_agent_state(new_agent_location)
        if state is None:
            return None
        return self.agent.get_state_action_value(state, action)

    def get_state_value_raw(
        self, new_agent_location: Tuple[int, int]
    ) -> Optional[float]:
        """Get the un-normalised value of the agent being in this location.

        Args:
            new_agent_location (Tuple[int, int]): _description_

        Returns:
            Optional[float]: the the raw value of the agent being in this
            location according to the agent.
        """
        state = self.__get_agent_state(new_agent_location)
        if state is None:
            return None
        return self.agent.get_state_value(state)

    def __get_agent_state(
        self, new_agent_location: Tuple[int, int]
    ) -> Union[int, None]:
        state_to_id = self.state_pool.state_to_id
        base_entities = self.entities

        best_state: Union[int, None] = None
        best_energy = 0

        for state, state_id in state_to_id.items():
            if state.agent_location != new_agent_location:
                continue
            if state.entities != base_entities:
                continue
            if state.agent_energy > best_energy:
                best_energy = state.agent_energy
                best_state = state_id
        return best_state
