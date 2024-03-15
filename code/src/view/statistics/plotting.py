import os
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QGridLayout, QPushButton, QWidget

from src.view.statistics.matplotlib_setup import (
    ThemeContext,
    ThemeContextManager,
    create_canvas,
)


class BasePlotter(object):
    """Class for providing plotting information."""

    def plot_data(self, axes: Axes):
        """Get the content for a plotting canvas.

        This can assume the canvas is clear.

        Args:
            axes (Axes): the axes to plot to.

        Raises:
            NotImplementedError: If this method is not overridden by a concrete
                class
        """
        raise NotImplementedError(
            "This method should be implemented in the concrete implementation"
        )


class PlottingCanvas(QWidget):
    """Canvas widget for displaying and saving charts."""

    save_text = "Save Plot"
    save_caption_text = "Save Plot Filename"
    save_file_format = "pdf"
    save_file_filter = "PDF (*.pdf)"
    save_size = 3

    def __init__(self, parent: Optional[QWidget], plotter: BasePlotter) -> None:
        """Initialise a plotting canvas.

        Args:
            parent (Optional[QWidget]): the parent this canvas should be
                rendered in.
            plotter (BasePlotter): the code responsible for doing the plotting

        Raises:
            RuntimeError: If there is an issue with
        """
        super().__init__(parent)

        layout = QGridLayout(self)
        self.plotter = plotter
        ThemeContextManager.update_theme_context(ThemeContext.application)
        self.figure = Figure()
        self.canvas = create_canvas(self.figure)
        layout.addWidget(self.canvas, 0, 0)
        axes = self.figure.subplots()
        if not isinstance(axes, Axes):
            raise RuntimeError("Incorrect axes object")
        self.axes = axes

        save_button = QPushButton(self.save_text, self)
        save_button.clicked.connect(self.__save_requested)
        layout.addWidget(save_button, 1, 0, Qt.AlignmentFlag.AlignRight)

    def request_update(self):
        """Request an update to refresh the data."""
        ThemeContextManager.update_theme_context(ThemeContext.application)
        self.axes.clear()
        self.plotter.plot_data(self.axes)
        self.canvas.draw()

    def __save_requested(self):
        path = QFileDialog.getSaveFileName(
            self, self.save_caption_text, os.getcwd(), self.save_file_filter
        )[0]
        ThemeContextManager.update_theme_context(ThemeContext.saving)
        save_figure = Figure((self.save_size * 2, self.save_size))
        save_axes = save_figure.subplots()
        if not isinstance(save_axes, Axes):
            raise RuntimeError("Incorrect axes object")
        self.plotter.plot_data(save_axes)

        if not path.endswith(self.save_file_format):
            path = f"{path}.{self.save_file_format}"
        save_figure.savefig(path, pad_inches=0.5, bbox_inches="tight")
