from src.model.config.grid_world_section import GridWorldConfig


class MockGridWorldConfig(GridWorldConfig):
    def __init__(self) -> None:
        pass

    @property
    def width(self) -> int:
        return 3

    @property
    def height(self) -> int:
        return 3

    @property
    def agent_location(self) -> tuple[int, int]:
        return 2, 1

    @property
    def entity_count(self) -> int:
        return 2
