from typing import Dict, Tuple

from src.model.agents.base_agent import BaseAgent
from src.model.dynamics.actions import Action
from src.model.state.state_instance import StateInstance
from src.model.state.state_pool import StatePool

from ..value_standardisation.value_range import ValueRange, ValueType

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
            agent (BaseAgent): the agent to decide the value.
            state_pool (StatePool): a state pool with all possible states.
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
    ) -> float:
        """Get the normalised value of a state and action.

        Args:
            state (StateInstance): the state to check.
            action (Action): the action to check.

        Returns:
            float: the value if one can be found.
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

    def get_state_value_normalised(self, state: StateInstance) -> float:
        """Get the normalised value of this state.

        Args:
            state (StateInstance): the state to check.

        Returns:
            float: the value of the state normalised.
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
