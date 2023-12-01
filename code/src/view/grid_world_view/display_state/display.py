from customtkinter import CTkFrame, CTkLabel

from src.model.dynamics.actions import Action
from src.view.icons.load_icon import IconLoader

from ....model.learning_system.state_description import StateDescription


class DisplayState(CTkFrame):
    """This widget contains the grid sizes it correctly.

    this widget sizes the view to fit as much of the container while maintaining
    the correct aspect ratio and centring the content
    """

    default_size = 0

    def __init__(self, master):
        """Initialise the padding widget.

        Args:
            master (Any): the widget to render this grid into
        """
        super().__init__(
            master, width=self.default_size, height=self.default_size
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.image_label = CTkLabel(self, text="")
        self.image_label.grid(row=1, column=0, sticky="nsew")
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def set_state(self, state: StateDescription):
        """Set the state to be displayed.

        Args:
            state (StateDescription): the state to be displayed
        """
        self.__configure_grid(self.winfo_width(), self.winfo_height())

    def resize(self, event):
        """Handle resize event.

        resize the inner grid based upon the updated dimensions.

        Args:
            event (Any): the resize event
        """
        self.__configure_grid(event.width, event.height)

    def __configure_grid(self, width: int, height: int):
        image = IconLoader().get_action_icon(Action.up, max(width // 2, 1))
        self.image_label.configure(image=image)
