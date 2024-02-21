from typing import Optional, Tuple

import numpy as np
from matplotlib.axes import Axes
from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.model.learning_system.learning_instance.statistics_record import (
    StatisticsRecord,
)
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.statistics.plotting import BasePlotter, PlottingCanvas
from src.view.visibility_observer import BaseVisibilityObserver


class RewardHistory(BaseVisibilityObserver, BasePlotter):
    """Widget for displaying the historical reward history."""

    def __init__(self, parent: Optional[QWidget]) -> None:
        """Initialise the reward history widget.

        uses matplotlib to create graphs.

        Args:
            parent (Optional[QWidget]): _description_

        Raises:
            RuntimeError: If there is an issue with matplotlib.
        """
        super().__init__(parent)

        layout = QGridLayout(self)

        self.canvas = PlottingCanvas(self, self)
        layout.addWidget(self.canvas, 0, 0)

        self.current_stats: Optional[StatisticsRecord] = None

    min_window_size = 3
    preferred_window_steps = 50

    @override
    def plot_data(self, axes: Axes):
        """Get the content for the plotting canvas.

        Args:
            axes (Axes): the axes to plot to.
        """
        axes.set_xlabel("Time steps")
        axes.set_ylabel("Reward")
        axes.set_title("Reward vs Time")
        if self.current_stats is None:
            return

        time_steps = self.current_stats.time_step
        x_axis = np.arange(time_steps)
        y_axis = np.array(self.current_stats.reward_history)
        axes.plot(
            x_axis,
            y_axis,
            "ro",
            label="Rewards",
        )

        if time_steps > self.min_window_size:
            window_size = int(
                max(
                    self.min_window_size,
                    time_steps / self.preferred_window_steps,
                ),
            )

            x_moving_average, y_moving_average = self.__moving_average(
                x_axis, y_axis, window_size
            )
            axes.plot(
                x_moving_average,
                y_moving_average,
                "b-",
                label=f"Moving Average, Width: {window_size}",
            )

        axes.legend(loc="upper left")

    @override
    def visible_state_updated(self, state: StateDescription) -> None:
        """Update the figure when new data is available.

        Args:
            state (StateDescription): the new state.
        """
        if state.statistics == self.current_stats:
            return
        self.current_stats = state.statistics
        self.canvas.request_update()

    def __moving_average(
        self, x_axis: np.ndarray, rewards: np.ndarray, window_size: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        # inspiration: https://stackoverflow.com/questions/14313510
        weights = np.repeat(1.0, window_size) / window_size
        moving_avg = np.convolve(rewards, weights, "valid")
        return x_axis[window_size - 2 : -1], moving_avg
