from typing import Tuple

from .base_section import BaseConfigSection


class GUIConfig(BaseConfigSection):
    """Gets configuration related to the GUI."""

    appearance_mode_property = "appearance_mode"
    color_theme_property = "color_theme"
    initial_size_section = "initial_size"
    width = "width"
    height = "height"

    def __init__(self) -> None:
        """Instantiate Grid world section config."""
        data_schema = {
            self.appearance_mode_property: str,
            self.color_theme_property: str,
            self.initial_size_section: {self.width: int, self.height: int},
        }

        super().__init__("gui", data_schema, [])

    @property
    def appearance_mode(self) -> str:
        """Get the theme style, e.g. light or dark.

        Returns:
            str: The theme style.
        """
        return self.configuration[self.appearance_mode_property]

    @property
    def color_theme(self) -> str:
        """Get the theme color.

        e.g "blue" (standard), "green", "dark-blue"


        Returns:
            str: The palate color.
        """
        return self.configuration[self.color_theme_property]

    @property
    def initial_size(self) -> Tuple[int, int]:
        """Get the initial size of the window.

        Returns:
            Tuple[int, int]: the width and hight of the window
        """
        section = self.configuration[self.initial_size_section]
        return (section[self.width], section[self.height])
