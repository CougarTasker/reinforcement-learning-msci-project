from schema import Schema

from .base_section import BaseConfigSection


class GridWorldConfig(BaseConfigSection):
    """Gets configuration related to the environment."""

    width_property = "width"
    height_property = "height"
    entity_count_property = "entity_count"
    energy_section = "energy"
    energy_capacity_property = "energy_capacity"
    initial_energy_property = "initial_energy"
    location_section = "agent_location"
    location_x_property = "x"
    location_y_property = "y"

    def __init__(self) -> None:
        """Instantiate Grid world section config."""
        data_schema = Schema(
            {
                self.width_property: int,
                self.height_property: int,
                self.entity_count_property: int,
                self.energy_section: {
                    self.energy_capacity_property: int,
                    self.initial_energy_property: int,
                },
                self.location_section: {
                    self.location_x_property: int,
                    self.location_y_property: int,
                },
            }
        )
        super().__init__("grid_world", data_schema)

    def width(self) -> int:
        """Get the default width of the grid world.

        Returns:
            int: the requested width
        """
        return self.configuration[self.width_property]

    def height(self) -> int:
        """Get the default height of the grid world.

        Returns:
            int: the requested height
        """
        return self.configuration[self.height_property]

    def agent_location(self) -> tuple[int, int]:
        """Get the default agent location.

        Returns:
            tuple[int, int]: the agents location x,y
        """
        pos_x = self.configuration[self.location_section][
            self.location_x_property
        ]
        pos_y = self.configuration[self.location_section][
            self.location_y_property
        ]
        return pos_x, pos_y

    def entity_count(self) -> int:
        """Get the number of entities to be spawned on the grid.

        Returns:
            int: The default number of entities to be spawned
        """
        return self.configuration[self.entity_count_property]

    def energy_capacity(self) -> int:
        """Get the energy capacity.

        Returns:
            int: the default energy capacity
        """
        return self.configuration[self.energy_section][
            self.energy_capacity_property
        ]

    def initial_energy(self) -> int:
        """Get the initial energy for the agent.

        Returns:
            int: the default initial energy
        """
        return self.configuration[self.energy_section][
            self.initial_energy_property
        ]
