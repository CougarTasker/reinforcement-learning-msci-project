from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivymd.color_definitions import colors

from . import primary_palette


class GridWorldView(Widget):
    def get_palette_color(self, hue):
        color = colors[primary_palette][str(hue)]

        def getColorComponent(start, end):
            return int(color[start:end], 16) / 255

        r = getColorComponent(0, 2)
        g = getColorComponent(2, 4)
        b = getColorComponent(4, 6)
        return Color(r=r, g=g, b=b)

    def __init__(self, rows=40, columns=60, margin=1, **kwargs):
        super(GridWorldView, self).__init__(**kwargs)
        self.rows = rows
        self.columns = columns
        self.margin = margin
        self.rectangles = [
            [Rectangle() for x in range(self.columns)] for y in range(self.rows)
        ]

        self.canvas.add(self.get_palette_color(800))
        for y in range(self.rows):
            for x in range(self.columns):
                self.canvas.add(self.rectangles[y][x])
        self.update_positions()
        self.bind(pos=self.update_positions, size=self.update_positions)

    def update_positions(self, *args):
        content_ratio = self.rows / self.columns
        container_ratio = self.size[1] / self.size[0]

        scale = (
            self.size[0] / self.columns
            if container_ratio > content_ratio
            else self.size[1] / self.rows
        )

        offsetX = (
            self.pos[0]
            + self.margin
            + (self.size[0] - self.columns * scale) / 2
        )
        offsetY = (
            self.pos[1] + self.margin + (self.size[1] - self.rows * scale) / 2
        )

        for y in range(self.rows):
            for x in range(self.columns):
                self.rectangles[y][x].pos = (
                    offsetX + scale * x,
                    offsetY + scale * y,
                )
                self.rectangles[y][x].size = (
                    scale - self.margin * 2,
                    scale - self.margin * 2,
                )
