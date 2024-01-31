# isort: skip_file
# flake8: noqa
import os

os.environ["QT_API"] = "pyside6"
import matplotlib

matplotlib.use("QtAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.pyplot import style, rcParams

style.use("dark_background")

# set transparent background
rcParams.update(
    {
        "figure.facecolor": (0.0, 0.0, 0.0, 0),
        "axes.facecolor": (0.0, 0.0, 0.0, 0),
    }
)


def create_canvas(figure: Figure) -> FigureCanvasQTAgg:
    """Method for getting canvas element.

    This method hides the setup for matplotlib backend that violates the linting
    rules

    Args:
        figure (Figure): the figure this canvas should display.

    Returns:
        FigureCanvasQTAgg: The canvas.
    """
    return FigureCanvasQTAgg(figure)
