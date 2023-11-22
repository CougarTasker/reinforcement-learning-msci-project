from customtkinter import CTkFrame

from ....controller.state_description import StateDescription
from .grid import InnerGrid


class DisplayState(CTkFrame):
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
        self.inner_grid = InnerGrid(self, state)

        self.set_state(state)
        self.inner_grid.grid(row=1, column=1, sticky="nsew")
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def set_state(self, state: StateDescription):
        """Set the state to be displayed.

        Args:
            state (StateDescription): the state to be displayed
        """
        self.aspect_ratio = state.grid_world.width / state.grid_world.height
        self.__configure_grid(self.winfo_width(), self.winfo_height())
        self.inner_grid.set_state(state)

    def resize(self, event):
        """Handle resize event.

        resize the inner grid based upon the updated dimensions.

        Args:
            event (Any): the resize event
        """
        self.__configure_grid(event.width, event.height)

    def __configure_grid(self, width: int, height: int):
        outer_aspect_ratio = width / height
        if outer_aspect_ratio < self.aspect_ratio:
            self.grid_columnconfigure((1), weight=1)
            self.grid_columnconfigure((0, 2), weight=0)

            inner_height = int(width / self.aspect_ratio)

            self.grid_rowconfigure((1), weight=0, minsize=inner_height)
            self.grid_rowconfigure((0, 2), weight=1)
        else:
            self.grid_rowconfigure((1), weight=1)
            self.grid_rowconfigure((0, 2), weight=0)

            inner_width = int(height * self.aspect_ratio)

            self.grid_columnconfigure((1), weight=0, minsize=inner_width)
            self.grid_columnconfigure((0, 2), weight=1)
