from schema import Schema
from .base_section import BaseConfigSection


class GridWorldConfig(BaseConfigSection):
    WIDTH_KEY = "width"
    HEIGHT_KEY = "height"

    def __init__(self) -> None:
        dataSchema = Schema({self.WIDTH_KEY: int, self.HEIGHT_KEY: int})
        super().__init__("grid_world", dataSchema)

    def width(self):
        return self.data[self.WIDTH_KEY]

    def height(self):
        return self.data[self.HEIGHT_KEY]
