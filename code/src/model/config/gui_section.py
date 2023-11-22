from schema import Schema

from .base_section import BaseConfigSection


class GUIConfig(BaseConfigSection):
    """Gets configuration related to the GUI."""

    appearance_mode_property = "appearance_mode"
    color_theme_property = "color_theme"

    def __init__(self) -> None:
        """Instantiate Grid world section config."""
        data_schema = Schema(
            {
                self.appearance_mode_property: str,
                self.color_theme_property: str,
            }
        )
        super().__init__("gui", data_schema)

    def appearance_mode(self) -> str:
        """Get the theme style, e.g. light or dark.

        Returns:
            str: The theme style.
        """
        return self.configuration[self.appearance_mode_property]

    def color_theme(self) -> str:
        """Get the theme color.

        e.g "blue" (standard), "green", "dark-blue"


        Returns:
            str: The palate color.
        """
        return self.configuration[self.color_theme_property]
