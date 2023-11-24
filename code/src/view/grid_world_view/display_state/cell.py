from typing import Optional

from colour import Color
from customtkinter import CTkFrame, CTkImage, CTkLabel

from src.controller.cell_configuration import CellConfiguration
from src.model.state.cell_entities import CellEntity

from ...icons.load_icon import IconLoader


class Cell(CTkFrame):
    """Widget to display an individual cell."""

    icon_padding = 6
    icon_relative_size = 0.7
    default_background_color = "grey30"

    def __init__(self, master, cell_config: CellConfiguration):
        """Initialise the cell.

        displays the cell as a rounded rectangle with an icon if the cell is not
        empty.

        Args:
            master (Any): the parent grid to draw this cell into
            cell_config (CellConfiguration): the configuration of how this cell
            should present.
        """
        super().__init__(
            master,
            border_color=self.default_background_color,
            border_width=self.icon_padding // 2,
            fg_color=self.default_background_color,
            width=0,
            height=0,
        )

        self.grid_propagate(False)
        self.label: Optional[CTkLabel] = None
        self.icon: Optional[CTkImage] = None
        self.cell_config: Optional[CellConfiguration] = None
        self.set_cell_configuration(cell_config)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def set_cell_configuration(self, cell_config: CellConfiguration):
        """Change the cell's current configuration.

        Args:
            cell_config (CellConfiguration): the new configuration of this cell
        """
        self.set_entity(cell_config.cell_entity)
        self.set_background_color(cell_config)
        self.cell_config = cell_config

    def set_background_color(self, cell_config: CellConfiguration):
        """Set the background color of this cell.

        Args:
            cell_config (CellConfiguration): the new configuration of the cell
            used to determine the colouration.
        """
        cell_color = self.__cell_color(cell_config.cell_value)
        if cell_config.cell_entity is CellEntity.empty:
            self.configure(border_color=cell_color, fg_color=cell_color)
        else:
            self.configure(
                border_color=cell_color, fg_color=self.default_background_color
            )

    def set_entity(self, entity: CellEntity):
        """Update the current entity.

        Args:
            entity (CellEntity): the new entity this cell should represent.
        """
        cell_entity_not_changed = (
            self.cell_config is not None
            and self.cell_config.cell_entity is entity
        )
        if cell_entity_not_changed:
            return
        if self.label is not None:
            self.label.destroy()
        if entity is CellEntity.empty:
            self.label = None
            self.icon = None
            return
        self.icon = IconLoader().get_cell_entity_icon(entity)
        self.label = CTkLabel(self, image=self.icon, text="")
        self.label.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=self.icon_padding,
            padx=self.icon_padding,
        )

    def resize(self, event):
        """Handle the resize event.

        updates the icon size to fit the cell.

        Args:
            event (Any): he resize event, providing the new size of the cell.
        """
        if self.icon is None or self.label is None:
            return
        cell_size = min(event.width, event.height)
        image_size = int(
            min(
                self.icon_relative_size * cell_size,
                max(cell_size - self.icon_padding, 1),
            ),
        )

        self.icon.configure(size=(image_size, image_size))
        self.label.configure(image=self.icon)

    def __cell_color(self, cell_value: Optional[float]) -> str:
        """Get the color the cell should be based upon the value.

        red represents a low value and green represents a good value

        Args:
            cell_value (Optional[float]): the value to calculate the color for

        Returns:
            str: the hex color of the cell based on this value.
        """
        if cell_value is None:
            return self.default_background_color

        # I know red is zero but this allows for more configuration
        start = Color("red").get_hue()
        end = Color("green").get_hue()

        hue = cell_value * (end - start) + start

        return Color(hsl=(hue, 1, 0.5)).hex_l
