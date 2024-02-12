# isort: skip_file
# flake8: noqa
import os

os.environ["QT_API"] = "pyside6"
import matplotlib

matplotlib.use("QtAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.pyplot import style, rcParams
import seaborn as sns


sns.set_theme(
    style="darkgrid",
    rc={
        "axes.edgecolor": "white",
        "axes.facecolor": ".2",
        "axes.labelcolor": "white",
        "figure.facecolor": (0.0, 0.0, 0.0, 0),
        "grid.color": "#202124",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "figure.constrained_layout.use": True,
    },
)
sns.set_context("notebook", rc={"grid.linewidth": 2})


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
