from src.model.transition_information import TransitionInformation

from .statistics_record import StatisticsRecord


class StatisticsRecorder(object):
    """Class for containing and recording statistics."""

    def __init__(self) -> None:
        """Initialise the statistics recorder."""
        self.statistics = StatisticsRecord(0, [], 0)

    def get_statistics(self) -> StatisticsRecord:
        """Get the current statics information.

        Returns:
            StatisticsRecord: object that represents the statistic information.
        """
        return self.statistics

    def record_transition(self, transition: TransitionInformation) -> None:
        """Record the information from a transition.

        Args:
            transition (TransitionInformation) : the transition information.
        """
        reward = transition.reward
        stats = self.statistics
        self.statistics = StatisticsRecord(
            stats.time_step + 1,
            [*stats.reward_history, reward],
            stats.total_reward + reward,
        )
