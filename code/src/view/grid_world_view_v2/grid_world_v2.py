from typing import Optional

from PySide6.QtWidgets import QGridLayout, QWidget
from typing_extensions import override

from src.controller.learning_system_controller import LearningSystemController
from src.model.learning_system.state_description.state_description import (
    StateDescription,
)
from src.view.grid_world_view_v2.display_state_v2.display import DisplayState
from src.view.grid_world_view_v2.interaction_controls import InteractionControls
from src.view.state_publisher import BaseStateObserver


class GridWorld(QWidget, BaseStateObserver):
    """This component combines a display with its controls.

    this widget represents a complete interface grid based agents.
    """

    def __init__(
        self, parent: Optional[QWidget], controller: LearningSystemController
    ) -> None:
        """Initialise the grid world agent.

        Args:
            parent (Optional[QWidget]): the parent widget this view should be
                mounted within.
            controller (LearningSystemController): Notify this controller when
                the user selects controls.
        """
        super().__init__(parent)
        layout = QGridLayout(self)

        self.display = DisplayState(self)
        layout.addWidget(self.display, 0, 0)
        layout.setRowStretch(0, 1)

        self.controls = InteractionControls(self, controller)
        layout.addWidget(self.controls, 1, 0)

    @override
    def state_updated(self, state: StateDescription):
        """Handle state update events.

        Args:
            state (StateDescription): the new state

        """
        self.display.set_state(state)
