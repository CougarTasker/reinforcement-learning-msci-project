from typing import Optional

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.model.learning_system.learning_instance.statistics_record import (
    StatisticsRecord,
)
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.statistics.matplotlib_setup import create_canvas
from src.view.visibility_observer import BaseVisibilityObserver


class RewardHistory(BaseVisibilityObserver):
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

        self.figure = Figure()
        self.canvas = create_canvas(self.figure)
        layout.addWidget(self.canvas, 0, 0)
        axes = self.figure.subplots()
        if not isinstance(axes, Axes):
            raise RuntimeError("Incorrect axis object")

        self.axes = axes
        self.__reset_plot()

        self.current_stats: Optional[StatisticsRecord] = None

    min_window_size = 3
    max_window_size = 50
    preferred_window_steps = 100

    @override
    def visible_state_updated(self, state: StateDescription) -> None:
        """Update the figure when new data is available.

        Args:
            state (StateDescription): the new state.
        """
        if state.statistics == self.current_stats:
            return
        self.current_stats = state.statistics
        time_steps = state.statistics.time_step
        self.__reset_plot()
        x_axis = np.arange(time_steps)
        y_axis = np.array(state.statistics.reward_history)
        self.axes.plot(
            x_axis,
            y_axis,
            "b-",
            label="Rewards",
        )

        if time_steps > self.min_window_size:
            window_size = int(
                min(
                    self.max_window_size,
                    max(
                        self.min_window_size,
                        time_steps / self.preferred_window_steps,
                    ),
                )
            )
            self.axes.plot(
                x_axis,
                self.__moving_average(y_axis, window_size),
                "r-",
                label=f"Moving Average, Width: {window_size}",
            )

        self.axes.legend()
        self.canvas.draw()

    def __moving_average(
        self, rewards: np.ndarray, window_size: int
    ) -> np.ndarray:
        # inspiration: https://stackoverflow.com/questions/14313510
        weights = np.repeat(1.0, window_size) / window_size
        moving_avg = np.convolve(rewards, weights, "valid")
        padding = np.zeros(window_size - 1)

        return np.concatenate((padding, moving_avg))

    def __reset_plot(self):
        self.axes.clear()
        self.axes.set_xlabel("Time steps")
        self.axes.set_ylabel("Reward")
        self.axes.set_title("Reward vs Time")
