from customtkinter import CTkFrame, CTkLabel

from src.model.state.cell_entities import CellEntity

from ...controller.state_description import StateDescription
from ..icons.load_icon import Icon, IconLoader


class GridPadding(CTkFrame):
    """This widget contains the grid sizes it correctly.

    this widget sizes the view to fit as much of the container while maintaining
    the correct aspect ratio and centring the content
    """

    default_size = 800

    def __init__(self, master, state: StateDescription):
        """Initialise the padding widget.

        Args:
            master (Any): the widget to render this grid into
            state (StateDescription): the current state to display
        """
        super().__init__(
            master, width=self.default_size, height=self.default_size
        )
        self.grid_propagate(False)
        self.aspect_ratio = state.grid_world.width / state.grid_world.height
        self.inner = GridWorldView(self, state)

        self.inner.grid(row=1, column=1, sticky="nsew")
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def resize(self, event):
        """Handle resize event.

        resize the inner grid based upon the updated dimensions.

        Args:
            event (Any): the resize event
        """
        outer_aspect_ratio = event.width / event.height
        if outer_aspect_ratio < self.aspect_ratio:
            self.grid_columnconfigure((1), weight=1)
            self.grid_columnconfigure((0, 2), weight=0)

            inner_height = int(event.width / self.aspect_ratio)

            self.grid_rowconfigure((1), weight=0, minsize=inner_height)
            self.grid_rowconfigure((0, 2), weight=1)

        else:
            self.grid_rowconfigure((1), weight=1)
            self.grid_rowconfigure((0, 2), weight=0)

            inner_width = int(event.height * self.aspect_ratio)

            self.grid_columnconfigure((1), weight=0, minsize=inner_width)
            self.grid_columnconfigure((0, 2), weight=1)


class GridWorldView(CTkFrame):
    """Positions the grid of cells."""

    def __init__(self, master, state: StateDescription):
        """Initialise the Grid World View.

        creates and positions each cell in a state.

        Args:
            master (_type_): the component to draw this in. use the
            `GridPadding` to maintain the correct aspect ratio.
            state (StateDescription): the state to display
        """
        super().__init__(master, fg_color="transparent", width=0, height=0)
        self.grid_propagate(False)
        self.set_state(state)
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    cell_padding = 3

    def resize(self, event):
        """Handle the resize event.

        used to update the column sizes

        Args:
            event (Any): the resize event, providing the new size of the grid.
        """
        number_of_columns = self.state.grid_world.width
        number_of_rows = self.state.grid_world.height
        cell_width = event.width // number_of_columns
        cell_height = event.height // number_of_rows
        cell_size = min(cell_width, cell_height)
        cell_size_inner = cell_size - self.cell_padding

        for row in range(number_of_rows):
            self.grid_rowconfigure(index=row, weight=0, minsize=cell_size_inner)

        for column in range(number_of_columns):
            self.grid_columnconfigure(
                index=column, weight=0, minsize=cell_size_inner
            )

    def set_state(self, state: StateDescription):
        """Set the current state to display.

        Args:
            state (StateDescription): the state to display
        """
        self.state = state

        for cell in state.grid_world.list_cells():
            column, row = cell
            Cell(self, state.cell_entity(cell)).grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=self.cell_padding,
                pady=self.cell_padding,
            )


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
