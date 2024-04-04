from cProfile import label

import numpy as np
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

sns.set_theme(
    context="notebook",
    style="darkgrid",
    rc={
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": "cmr10",
        "axes.formatter.use_mathtext": True,
    },
)

filename = "example-curve.pdf"
save_size = 3


save_figure = Figure((save_size * 2, save_size))

save_axes = save_figure.subplots()

if not isinstance(save_axes, Axes):
    raise RuntimeError("Incorrect axes object")

save_axes.set_title(r"$\varepsilon_t = \lambda^t \cdot \varepsilon_0$")
save_axes.set_ylabel(r"$\varepsilon_t$")
save_axes.set_xlabel(r"$\lambda$")


def plot_power(power: int):
    x_axis = np.power(np.linspace(0, 1, 100), float(1) / 8)
    y_axis = np.power(x_axis, power)
    save_axes.plot(x_axis, y_axis, "-", label=f"$t = {power}$")


plot_power(5000)
plot_power(500)
plot_power(50)

save_axes.legend()

save_figure.savefig(filename, pad_inches=0.5, bbox_inches="tight")
