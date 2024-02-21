# isort: skip_file
# flake8: noqa
from enum import Enum
import os

os.environ["QT_API"] = "pyside6"
import matplotlib

matplotlib.use("QtAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import seaborn as sns


class ThemeContext(Enum):
    application = 0
    saving = 1
    not_set = 2


class ThemeContextManager(object):
    current_theme_context = ThemeContext.not_set

    @classmethod
    def update_theme_context(cls, desired_context: ThemeContext) -> None:
        if desired_context is cls.current_theme_context:
            return
        sns.reset_defaults()
        match desired_context:
            case ThemeContext.application:
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
            case ThemeContext.saving:
                sns.set_theme(style="darkgrid")


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
