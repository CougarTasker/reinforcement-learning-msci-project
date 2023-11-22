from customtkinter import CTkFrame

from ....controller.state_description import StateDescription
from .cell import Cell


class InnerGrid(CTkFrame):
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

        for row in range(number_of_rows):
            self.grid_rowconfigure(index=row, weight=0, minsize=cell_size)

        for column in range(number_of_columns):
            self.grid_columnconfigure(index=column, weight=0, minsize=cell_size)

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
