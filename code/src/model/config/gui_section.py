from schema import Schema

from .base_section import BaseConfigSection


class GUIConfig(BaseConfigSection):
    """Gets configuration related to the GUI."""

    grid_view_background_hue_property = "grid_view_background_hue"
    theme_style_property = "theme_style"
    theme_palette_property = "primary_palette"

    def __init__(self) -> None:
        """Instantiate Grid world section config."""
        data_schema = Schema(
            {
                self.theme_style_property: str,
                self.theme_palette_property: str,
                self.grid_view_background_hue_property: int,
            }
        )
        super().__init__("gui", data_schema)

    def theme_style(self) -> str:
        """Get the theme style, e.g. light or dark.

        Returns:
            str: The theme style.
        """
        return self.configuration[self.theme_style_property]

    def theme_palette(self) -> str:
        """Get the theme palette.

        This is the color scheme for this application.

        Returns:
            str: The palate color.
        """
        return self.configuration[self.theme_palette_property]

    def grid_view_background_hue(self) -> int:
        """Get the hue for the background of the grid world view.

        Returns:
            int: The background hue for the grid world view.
        """
        return self.configuration[self.grid_view_background_hue_property]
