from typing import Optional

from src.model.agents.base_agent import BaseAgent
from src.model.agents.value_iteration.dynamics_distribution import (
    DynamicsDistribution,
)
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.state.state_pool import StatePool

from .normaliser import StateValueNormaliser
from .value_range import ValueRange


class NormaliserFactory(object):
    """Factory class for creating value normalisers."""

    def __init__(
        self, agent: BaseAgent, dynamics: BaseDynamics, enable_cache: bool
    ) -> None:
        """Initialise the normaliser factory.

        This factory creates normalisers and caches equivalent ones to avoid
        re-computation

        Args:
            agent (BaseAgent): the agent to generate normalisers for
            dynamics (BaseDynamics): the dynamics to generate normalisers for
            enable_cache: weather the cache can be enabled (if the value table
                changes like for q-learning then caching must be disabled)
        """
        self.agent = agent
        self.dynamics = dynamics
        self.has_generated_all_states: bool = False
        self.cache: Optional[StateValueNormaliser] = None
        self.value_range: Optional[ValueRange] = None
        self.enable_cache = enable_cache

    def create_normaliser(self, base_state: int) -> StateValueNormaliser:
        """Get the appropriate state normaliser for the given base state.

        Args:
            base_state (int): the state the defines the possible entities that
                the normaliser should consider.

        Returns:
            StateValueNormaliser: _description_
        """
        entities = self.dynamics.state_pool.get_state_from_id(
            base_state
        ).entities
        if self.cache is not None and self.enable_cache:
            return self.cache

        normaliser = StateValueNormaliser(
            self.agent,
            self.__get_state_pool(),
            self.__get_value_range(),
        )
        self.cache = normaliser
        return normaliser

    def __get_state_pool(self) -> StatePool:
        """Get a fully populated state pool.

        Returns:
            StatePool: the pool of all possible reachable states
        """
        if self.has_generated_all_states:
            return self.dynamics.state_pool
        # use the dynamics distribution code to ensure all states are visited
        dd = DynamicsDistribution(100, self.dynamics)
        dd.compile()
        self.has_generated_all_states = True
        return self.dynamics.state_pool

    def __get_value_range(self) -> ValueRange:
        """Get the value range for this given dynamics and agent.

        Returns:
            ValueRange: the range of values to provide a consistent scale
        """
        if self.value_range is not None and self.enable_cache:
            return self.value_range

        self.value_range = ValueRange(self.__get_state_pool(), self.agent)
        return self.value_range
