from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivymd.color_definitions import colors

from ..model.config.gui_section import GUIConfig


class GridWorldView(Widget):
    """A kivy widget for displaying and editing simple grid world states."""

    def __init__(self, config: GUIConfig, **kwargs):
        """Initialise a new Grid World View widget.

        Args:
            config (GUIConfig): the configuration used to display the graphics
            kwargs: arguments for the base kivy widget.
        """
        super().__init__(**kwargs)
        self.rows = 9
        self.columns = 16
        self.margin = 1
        self.rectangles = [
            [Rectangle() for column in range(self.columns)]
            for row in range(self.rows)
        ]
        self.config = config
        self.canvas.add(
            self.get_palette_color(config.grid_view_background_hue())
        )
        for row in range(self.rows):
            for col in range(self.columns):
                self.canvas.add(self.rectangles[row][col])
        self.update_positions()
        self.bind(pos=self.update_positions, size=self.update_positions)

    eight_bit_color_range = 255
    hexadecimal_base = 16

    def get_palette_color(self, hue: int) -> Color:
        """Create color from theme palette.

        A utility method for generating color objects from theme colors.

        Args:
            hue (int): the hue of the theme color to select

        Returns:
            Color: the kivy color object representing that color
        """
        color = colors[self.config.theme_palette()][str(hue)]

        def get_color_component(start, end):
            return (
                int(color[start:end], self.hexadecimal_base)
                / self.eight_bit_color_range
            )

        red = get_color_component(0, 2)
        green = get_color_component(2, 4)
        blue = get_color_component(4, 6)
        return Color(r=red, g=green, b=blue)

    def update_positions(self, *args):
        """Update rectangle positions after resize.

        Args:
            args: the unused arguments passed from binding, required or will
            through error.
        """
        content_ratio = self.rows / self.columns
        container_ratio = self.size[1] / self.size[0]

        scale = (
            self.size[0] / self.columns
            if container_ratio > content_ratio
            else self.size[1] / self.rows
        )

        offset_x = self.pos[0]
        offset_x += (self.size[0] - self.columns * scale) / 2

        offset_y = self.pos[1]
        offset_y += (self.size[1] - self.rows * scale) / 2

        for row in range(self.rows):
            for col in range(self.columns):
                self.rectangles[row][col].pos = (
                    offset_x + scale * col,
                    offset_y + scale * row,
                )
                self.rectangles[row][col].size = (
                    scale - self.margin,
                    scale - self.margin,
                )
