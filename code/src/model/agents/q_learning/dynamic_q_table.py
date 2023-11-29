from typing import Dict, Tuple

import numpy as np

from src.model.dynamics.actions import Action


class DynamicQTable(object):
    """Class for storing and recalling action-state values."""

    def __init__(self, learning_rate: float) -> None:
        """Initialise a new blank Q Table.

        Args:
            learning_rate (float): the rate at which to change the value with
            each update.
        """
        self.table: Dict[Tuple[int, Action], float] = {}
        self.learning_rate = learning_rate

    def update_value(self, state: int, action: Action, q_value: float):
        """Update the value at state and action based upon some observation.

        the amount the value is changed depends on the magnitude of the learning
        rate.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to update the value for
            q_value (float): the new observation of the Q value
        """
        existing_value = self.get_value(state, action)
        new_value = existing_value + self.learning_rate * (
            q_value - existing_value
        )
        self.set_value(state, action, new_value)

    def set_value(self, state: int, action: Action, q_value: float):
        """Set the value of a given state action pair.

        This will overwrite any existing data.

        Args:
            state (int): the state the action is performed in
            action (Action): the action to update the value for
            q_value (float): the new value of this state action pair.
        """
        self.table[(state, action)] = q_value

    def get_value(self, state: int, action: Action) -> float:
        """Get the current value of a give state and action.

        if the state and action has no existing value associated with it then a
          new value in the range 0-1 will be chosen

        Args:
            state (int): the state the action is performed in
            action (Action): the action to get the value for

        Returns:
            float: current stored value at the given state-action pair.
        """
        key = (state, action)
        existing_value = self.table.get(key, None)
        if existing_value is not None:
            return existing_value
        new_value = self.__default_value()
        self.table[key] = new_value
        return new_value

    def __default_value(self) -> float:
        return np.random.rand()
