from dataclasses import replace

from src.model.transition_information import TransitionInformation

from .statistics_record import StatisticsRecord


class StatisticsRecorder(object):
    """Class for containing and recording statistics."""

    def __init__(self) -> None:
        """Initialise the statistics recorder."""
        self.statistics = StatisticsRecord(0, [], 0, None)

    def set_current_state(self, state_id: int) -> None:
        """Set the current state to a specific value.

        Used for resting the state without a traditional transition.

        Args:
            state_id (int): the new state of the simulation.
        """
        self.statistics = replace(self.statistics, current_state=state_id)

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
            transition.new_state,
        )
