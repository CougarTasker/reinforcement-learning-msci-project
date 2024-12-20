import sys

from ..config.grid_world_section import GridWorldConfig
from ..state.state_instance import StateInstance
from ..state.state_pool import StatePool
from .actions import Action
from .grid_world import GridWorld


class BaseDynamics(object):
    """The abstract base class for dynamics classes.

    This class provides the basic methods a dynamics class is expected to
    implement and some common functionality
    """

    def __init__(self, config: GridWorldConfig) -> None:
        """Instantiate a dynamics, provides the minimal required properties.

        Args:
            config (GridWorldConfig): the config used by this dynamics such as
                the size of the grid world.
        """
        self.state_pool = StatePool()
        self.config = config
        self.grid_world = GridWorld(config.width, config.height)

    def is_stochastic(self) -> bool:
        """Determine weather the dynamics behave stochastically.

        If stochastic then there is random variability in the output of `next`.
        However variability distribution must still be markovian.

        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            bool: weather this dynamics behaves stochastically.

        """
        raise NotImplementedError(
            "This method must be overridden by concrete dynamics classes"
        )

    def state_count_upper_bound(self) -> int:
        """Get an upper bound on the number of states.

        used for pre-allocating memory.

        Returns:
            int: an upper bound on the number of state.
        """
        return sys.maxsize

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            StateInstance: the starting state.
        """
        raise NotImplementedError(
            "This method must be overridden by concrete dynamics classes"
        )

    def next(
        self, current_state: StateInstance, action: Action
    ) -> tuple[StateInstance, float]:
        """Compute the next state and reward.

        Must only compute the next reward and state based on only the provided
        current state and reward to obey the markov property.

        Args:
            current_state (StateInstance): the state that the action is
                performed in
            action (Action): the action the agent has chosen


        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            tuple[StateInstance, float]: the resulting state after the action
            has been performed and the reward from this action
        """
        raise NotImplementedError(
            "This method must be overridden by concrete dynamics classes"
        )

    def initial_state_id(self) -> int:
        """Provide the initial state id of this environment.

        Raises:
            NotImplementedError: If this method has not been overridden

        Returns:
            int: the starting state id.
        """
        return self.state_pool.get_state_id(self.initial_state())

    def next_state_id(
        self, current_state_id: int, action: Action
    ) -> tuple[int, float]:
        """Compute the next state and reward.

        Must only compute the next reward and state based on only the provided
        current state and reward to obey the markov property.

        Args:
            current_state_id (int): the state that the action is
                performed in
            action (Action): the action the agent has chosen


        Raises:
            NotImplementedError: If this method has not been overridden

        Returns:
            tuple[int, float]: the resulting state after the action has been
            performed and the reward from this action
        """
        current_state = self.state_pool.get_state_from_id(current_state_id)
        next_state, reward = self.next(current_state, action)
        return self.state_pool.get_state_id(next_state), reward
