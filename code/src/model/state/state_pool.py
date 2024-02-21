from typing import Dict

from .state_instance import StateInstance


class StatePool(object):
    """Class that manages the creation of states.

    This class avoids redundant states and allows for consistent identification
    """

    def __init__(self) -> None:
        """Initialise a state pool."""
        self.id_to_state: Dict[int, StateInstance] = {}
        self.state_to_id: Dict[StateInstance, int] = {}

    def is_existing_state(self, state: StateInstance) -> bool:
        """Determine weather a state has already been registered.

        Args:
            state (StateInstance): the state to check

        Returns:
            bool: true if this state already exists in this pool
        """
        return state in self.state_to_id

    def get_state_id(self, state: StateInstance) -> int:
        """Get the numeric id for a given state.

        If the state has already been registered with this pool then it should
        return the existing key. else it should add this state to the pool and
        return the new state.

        Note, this id is not necessarily globally unique however it is unique in
        this state pool

        Args:
            state (StateInstance): the state to get a unique id for

        Returns:
            int: the id for this state
        """
        state_to_id = self.state_to_id
        if state in state_to_id:
            return state_to_id[state]  # noqa: WPS529 get is too slow
        new_id = len(state_to_id)
        state_to_id[state] = new_id
        self.id_to_state[new_id] = state
        return new_id

    def get_state_from_id(self, identifier: int) -> StateInstance:
        """Get the state object corresponding to the given key in this pool.

        Args:
            identifier (int): the key of the state to get

        Returns:
            StateInstance: the state that is registered under this id
        """
        return self.id_to_state[identifier]
