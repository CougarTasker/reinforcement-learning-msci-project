from customtkinter import CTkFrame, CTkLabel

from src.model.state.cell_entities import CellEntity

from ...icons.load_icon import Icon, IconLoader


class Cell(CTkFrame):
    """Widget to display an individual cell."""

    icon_padding = 5
    icon_relative_size = 0.7

    def __init__(self, master, entity: CellEntity):
        """Initialise the cell.

        displays the cell as a rounded rectangle with an icon if the cell is not
        empty.

        Args:
            master (_type_): the parent grid to draw this cell into
            entity (CellEntity): the entity that is in this cell.
        """
        super().__init__(master, fg_color="grey30", width=0, height=0)
        self.grid_propagate(False)
        self.entity = entity
        if self.entity is CellEntity.empty:
            return
        self.icon = IconLoader().get_icon(self.icon_type())
        self.label = CTkLabel(self, image=self.icon, text="")
        self.label.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=self.icon_padding,
            padx=self.icon_padding,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def resize(self, event):
        """Handle the resize event.

        updates the icon size to fit the cell.

        Args:
            event (Any): he resize event, providing the new size of the cell.
        """
        if self.entity is CellEntity.empty:
            return
        cell_size = min(event.width, event.height)
        image_size = int(
            min(
                self.icon_relative_size * cell_size,
                cell_size - self.icon_padding,
            )
        )

        self.icon.configure(size=(image_size, image_size))
        self.label.configure(image=self.icon)

    def icon_type(self) -> Icon:
        """Get the icon that represents each type of cell entity.

        Raises:
            ValueError: if the cell entity does not have a corresponding icon

        Returns:
            Icon: the icon that represents this cell's entity.
        """
        match self.entity:
            case CellEntity.agent:
                return Icon.robot
            case CellEntity.goal:
                return Icon.flag
            case CellEntity.blocked:
                return Icon.no_entry
            case _:
                raise ValueError(
                    f"entry {self.entity.name} is not valid for display"
                )
