from typing import Dict, Optional, Tuple

from customtkinter import CTkFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageDraw

from src.view.grid_world_view.display_state.cell.cell import Cell

from ....model.learning_system.state_description import StateDescription


class DisplayState(CTkFrame):
    """This widget contains the grid sizes it correctly.

    this widget sizes the view to fit as much of the container while maintaining
    the correct aspect ratio and centring the content
    """

    default_size = 0

    cell_margins = 0.1

    def __init__(self, master):
        """Initialise the padding widget.

        Args:
            master (Any): the widget to render this grid into
        """
        super().__init__(
            master, width=self.default_size, height=self.default_size
        )
        self.state: Optional[StateDescription] = None
        self.cells: Dict[Tuple[int, int], Cell] = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.figure.add_subplot()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def set_state(self, state: StateDescription):
        """Set the state to be displayed.

        Args:
            state (StateDescription): the state to be displayed
        """
        self.state = state
        width, height = self.winfo_width(), self.winfo_height()
        self.__configure_grid(width, height)

    def resize(self, event):
        """Handle resize event.

        resize the inner grid based upon the updated dimensions.

        Args:
            event (Any): the resize event
        """
        self.__configure_grid(event.width, event.height)

    def __populate_cells(
        self, state: StateDescription, width: int, height: int
    ):
        self.cells = {}

        cell_positions = state.grid_world.list_cell_positions(
            width, height, self.cell_margins
        )

        for cell_position in cell_positions:
            (
                cell_coordinate,
                bounding_box,
            ) = cell_position
            self.cells[cell_coordinate] = Cell(
                state.cell_config[cell_coordinate], bounding_box
            )

    background_color = (255, 5, 50)

    def __make_blank_image(self, width: int, height: int):
        image_mode = "RGB"
        image = Image.new(image_mode, (width, height), self.background_color)
        image_draw = ImageDraw.Draw(image, image_mode)
        return image, image_draw

    def __configure_grid(self, width: int, height: int):
        if self.state is None:
            return
        (
            expected_cell_size,
            _marin_size,
        ) = self.state.grid_world.get_cell_sizing(
            width, height, self.cell_margins
        )
        if expected_cell_size < 10:
            # cells are too small
            return
        self.__populate_cells(self.state, width, height)
        image, image_draw = self.__make_blank_image(width, height)

        for cell in self.cells.values():
            cell.draw(image, image_draw)

        self.plot.imshow(image)
        self.canvas.draw()
