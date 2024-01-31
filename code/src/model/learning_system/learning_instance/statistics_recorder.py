from src.model.dynamics.actions import Action

from .statistics_record import StatisticsRecord


class StatisticsRecorder(object):
    """Class for containing and recording statistics."""

    def __init__(self) -> None:
        """Initialise the statistics recorder."""
        self.statistics = StatisticsRecord(0, [])

    def get_statistics(self) -> StatisticsRecord:
        """Get the current statics information.

        Returns:
            StatisticsRecord: object that represents the statistic information.
        """
        return self.statistics

    def record_transition(
        self,
        previous_state: int,
        previous_action: Action,
        new_state: int,
        reward: float,
    ) -> None:
        """Record the information from a transition.

        Args:
            previous_state (int): the state before the action was taken
            previous_action (Action): the action that was taken.
            new_state (int): The resulting state after the action has been taken
            reward (float): the reward for performing this action
        """
        stats = self.statistics
        self.statistics = StatisticsRecord(
            stats.time_step + 1, [*stats.reward_history, reward]
        )
