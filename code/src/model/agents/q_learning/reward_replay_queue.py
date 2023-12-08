from typing import List, Tuple

from src.model.agents.q_learning.dynamic_q_table import DynamicQTable
from src.model.dynamics.actions import Action

#  previous_state,previous_action-> new_state, reward
observation_type = Tuple[int, Action, int, float]


class RewardReplayQueue(object):
    """A Queue for recording previous actions and replaying them.

    To allow for faster convergence and backwards propagation of value.
    """

    def __init__(
        self, q_table: DynamicQTable, queue_length: int, discount_rate: float
    ) -> None:
        """Create a new replay queue.

        Args:
            q_table (DynamicQTable): the q value table to update
            queue_length (int): the maximum length of the queue.
            discount_rate (float): the amount to discount future rewards.
        """
        self.max_queue_length = queue_length
        self.table = q_table
        self.queue: List[observation_type] = []
        self.discount_rate = discount_rate

    def add_observation(
        self,
        previous_state: int,
        previous_action: Action,
        new_state: int,
        reward: float,
    ):
        """Add a new observation to the end of the queue.

        Args:
            previous_state (int): the state before the action was taken
            previous_action (Action): the action that was taken.
            new_state (int): The resulting state after the action has been taken
            reward (float): the reward for performing this action
        """
        self.__add_item((previous_state, previous_action, new_state, reward))
        for observation in reversed(self.queue):
            self.__update_q_value(observation)

    def __update_q_value(self, observation: observation_type):
        (previous_state, previous_action, new_state, reward) = observation

        observed_value = (
            reward
            + self.discount_rate * self.table.calculate_state_value(new_state)
        )
        self.table.update_value(previous_state, previous_action, observed_value)

    def __add_item(self, observation: observation_type):
        self.queue.append(observation)
        if len(self.queue) > self.max_queue_length:
            self.queue.pop(0)
