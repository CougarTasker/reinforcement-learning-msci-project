class TestConfig:
    def width(self) -> int:
        return 3

    def height(self) -> int:
        return 3

    def agent_location(self) -> tuple[int, int]:
        return 2, 1

    def entity_count(self) -> int:
        return 2

    def energy_capacity(self) -> int:
        return 10

    def initial_energy(self) -> int:
        return 10
