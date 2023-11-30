from tkinter import CENTER, E, N, S, W  # noqa: WPS347
from typing import Any, Dict, Optional

from colour import Color
from customtkinter import CTkFrame, CTkImage, CTkLabel
from tktooltip import ToolTip

from src.model.dynamics.actions import Action
from src.model.state.cell_entities import CellEntity

from ....model.learning_system.cell_configuration import (
    CellConfiguration,
    DisplayMode,
    action_value_description,
)
from ...icons.load_icon import Icon, IconLoader


class Cell(CTkFrame):
    """Widget to display an individual cell."""

    icon_padding = 6
    icon_relative_size = 0.7
    default_background_color = "grey30"
    minimum_arrow_size = 0
    maximum_arrow_size = 0.4

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
        self.main_icon_label = CTkLabel(self, text="")
        self.main_icon_label.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER,
        )
        self.arrow_labels: Dict[Action, CTkLabel] = self.__setup_arrow_labels()
        self.cell_config: Optional[CellConfiguration] = None
        self.__create_tooltip(self)
        self.__create_tooltip(self.main_icon_label)
        self.set_cell_configuration(cell_config)
        self.bind(
            "<Configure>",
            command=self.resize,
        )

    def cell_size(self) -> int:
        """Get the size of this cell in pixels.

        Returns:
            int: the size of this cell in pixels
        """
        return min(self.winfo_width(), self.winfo_height())

    def set_cell_configuration(self, cell_config: CellConfiguration):
        """Change the cell's current configuration.

        Args:
            cell_config (CellConfiguration): the new configuration of this cell
        """
        self.update_main_icon(cell_config)
        self.update_arrows(cell_config)
        self.update_background_color(cell_config)
        self.cell_config = cell_config

    def get_tooltip_text(self) -> str:
        """Get the text to display if the user hovers over this cell.

        Returns:
            str: the text to display
        """
        if self.cell_config is None:
            return "loading"
        location = self.cell_config.location
        state_value = self.cell_config.cell_value_raw
        action_values = self.cell_config.action_values_raw

        tooltip_text = f"location={location}"
        if state_value is not None:
            tooltip_text += f"\nstate value={state_value:.3f}"
        for action, action_value in action_values.items():
            if action_value is not None:
                tooltip_text += (
                    f"\n{action.name} action value={action_value:.3f}"
                )
        return tooltip_text

    def update_background_color(self, cell_config: CellConfiguration):
        """Set the background color of this cell.

        Args:
            cell_config (CellConfiguration): the new configuration of the cell
            used to determine the colouration.
        """
        if cell_config.display_mode is not DisplayMode.state_value:
            self.configure(
                border_color=self.default_background_color,
                fg_color=self.default_background_color,
            )
            return

        cell_color = self.__cell_color(cell_config.cell_value_normalised)
        if cell_config.cell_entity is CellEntity.empty:
            self.configure(border_color=cell_color, fg_color=cell_color)
        else:
            self.configure(
                border_color=cell_color, fg_color=self.default_background_color
            )

    def update_main_icon(self, cell_config: CellConfiguration):
        """Update the size or image at the center of the cell.

        Args:
            cell_config (CellConfiguration): the new cell configuration that
            determines what icon to display.
        """
        cell_size = self.cell_size()
        image_size = int(
            max(
                min(
                    self.icon_relative_size * cell_size,
                    cell_size - self.icon_padding,
                ),
                1,
            ),
        )
        icon = self.__get_main_icon(cell_config, image_size)
        self.main_icon_label.configure(image=icon)

    no_arrows: action_value_description = {
        Action.up: None,
        Action.down: None,
        Action.left: None,
        Action.right: None,
    }

    def update_arrows(self, cell_config: CellConfiguration):
        """Update the size of the arrows.

        Args:
            cell_config (CellConfiguration): the configuration that determines
            the size of the arrows
        """
        match cell_config.display_mode:
            case (
                DisplayMode.default
                | DisplayMode.state_value
                | DisplayMode.best_action
            ):
                self.__update_arrow_sizes(self.no_arrows)
            case DisplayMode.action_value_global:
                self.__update_arrow_sizes(cell_config.action_values_normalised)
            case DisplayMode.action_value_local:
                self.__update_arrow_sizes(
                    self.__rescale_values_locally(cell_config.action_values_raw)
                )

    def resize(self, event):
        """Handle the resize event.

        updates the icon size to fit the cell.

        Args:
            event (Any): he resize event, providing the new size of the cell.
        """
        config = self.cell_config
        if config is None:
            return

        self.update_main_icon(config)
        self.update_arrows(config)

    def __rescale_values_locally(
        self, action_values: action_value_description
    ) -> action_value_description:
        """Rescale the action values in this cell 0-1.

        this should only be based on the values in this cell rather than the
        global range of values.

        Args:
            action_values (action_value_description): the action values of this
            cell.

        Returns:
            action_value_description: the scaled action values in the range 0-1
        """
        min_value = float("inf")
        max_value = float("-inf")

        for action_value in action_values.values():
            if action_value is None:
                continue
            min_value = min(action_value, min_value)
            max_value = max(action_value, max_value)

        rescaled_values: action_value_description = {}
        value_range = max_value - min_value
        for action, action_value in action_values.items():
            if action_value is None:
                rescaled_values[action] = None
                continue
            rescaled_values[action] = (action_value - min_value) / value_range
        return rescaled_values

    def __get_arrow_size(self, arrow_value: float) -> int:
        """Get the size of the arrow based upon its value and the cell's size.

        Args:
            arrow_value (float): the value of this arrow in the range 0-1

        Returns:
            int: the number of pixels this arrow should be
        """
        size_range = self.maximum_arrow_size - self.minimum_arrow_size
        size_relative = arrow_value * size_range + self.minimum_arrow_size
        cell_size = self.cell_size()
        # scale to pixels clamp to reenable bounds
        pixel_size = max(
            min(self.icon_relative_size * cell_size, cell_size * size_relative),
            1,
        )

        return int(pixel_size)

    empty_icon = IconLoader().get_icon(Icon.empty, 1)

    def __update_arrow_sizes(self, sizes: action_value_description):
        """Change the size of the arrows.

        the sizes are based upon the their values and the size of the cell.

        Args:
            sizes (action_value_description): the sizes of the arrows
        """
        for action in Action:
            action_value = sizes[action]
            arrow_label = self.arrow_labels[action]
            if action_value is None:
                arrow_label.place_forget()
                arrow_label.configure(image=self.empty_icon)
            else:
                scaled_icon = IconLoader().get_action_icon(
                    action, self.__get_arrow_size(action_value)
                )
                self.__place_arrow_label(action, arrow_label)
                arrow_label.configure(image=scaled_icon)

    def __get_main_icon(
        self, cell_config: CellConfiguration, size: int
    ) -> CTkImage:
        """Get what the main icon should be based upon the cell config.

        Args:
            cell_config (CellConfiguration): the configuration that determines
            the icon to show
            size (int): the size to show the icon.

        Returns:
            CTkImage: the image that corresponds to what the main icon should be
        """
        match cell_config.display_mode:
            case DisplayMode.default | DisplayMode.state_value:
                return IconLoader().get_cell_entity_icon(
                    cell_config.cell_entity, size
                )
            case (
                DisplayMode.action_value_global | DisplayMode.action_value_local
            ):
                if cell_config.cell_entity is CellEntity.goal:
                    return IconLoader().get_cell_entity_icon(
                        cell_config.cell_entity, size
                    )
                return self.empty_icon
            case DisplayMode.best_action:
                best_action = self.__get_best_action(
                    cell_config.action_values_raw
                )
                if best_action is None:
                    return IconLoader().get_cell_entity_icon(
                        cell_config.cell_entity, size
                    )

                return IconLoader().get_action_icon(best_action, size)

    def __get_best_action(
        self, action_values: action_value_description
    ) -> Optional[Action]:
        """Get the action that has the best value.

        Args:
            action_values (action_value_description): the values to determined
            the best action from.

        Returns:
            Optional[Action]: the best action if there is one.
        """
        best_action_value = float("-inf")
        best_action = None
        for action in Action:
            action_value = action_values[action]
            if action_value is None:
                continue
            if best_action_value is None:
                best_action_value = action_value
                best_action = action
            elif action_value > best_action_value:
                best_action_value = action_value
                best_action = action
        return best_action

    def __setup_arrow_labels(self) -> Dict[Action, CTkLabel]:
        """Create the arrow labels to contain the arrow icons.

        Returns:
            Dict[Action, CTkLabel]: the arrow icons
        """
        action_arrows: Dict[Action, CTkLabel] = {}

        for action in Action:
            label = CTkLabel(self, text="")
            self.__create_tooltip(label)
            action_arrows[action] = label

        return action_arrows

    def __place_arrow_label(self, action: Action, label: CTkLabel):
        """Position an arrow label based on the direction of its action.

        Args:
            action (Action): provides the direction the label should act in.
            label (CTkLabel): the label to be positioned
        """
        match action:
            case Action.up:
                label.place(relx=0.5, rely=0, anchor=N)
            case Action.down:
                label.place(relx=0.5, rely=1, anchor=S)
            case Action.left:
                label.place(relx=0, rely=0.5, anchor=W)
            case Action.right:
                label.place(relx=1, rely=0.5, anchor=E)

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

    def __create_tooltip(self, master: Any) -> ToolTip:
        """Create a tooltip.

        create a tooltip themed consistently. a new tooltip needs to be created
        for every widget in this cell so no matter where the cursor is in the
        cell the tooltip is shown.

        Args:
            master (Any): the element to attach it to

        Returns:
            ToolTip: the tooltip object that has been created
        """
        return ToolTip(
            master,
            msg=self.get_tooltip_text,
            parent_kwargs={"bg": "black", "padx": 5, "pady": 5},
            fg="#ffffff",
            bg="#1c1c1c",
            padx=10,
            pady=10,
        )
