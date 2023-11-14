from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar.toolbar import MDTopAppBar

from ..model.config.reader import ConfigReader
from .grid_world_view import GridWorldView


class ReinforcementLearningApp(MDApp):
    """The root of the GUI.

    The highest level widget of the GUI.
    """

    def build(self):
        """Initialise the GUI.

        Returns:
            Widget: the widget tree to be rendered
        """
        config = ConfigReader().gui()
        self.theme_cls.theme_style = config.theme_style()
        self.theme_cls.primary_palette = config.theme_palette()
        return MDBoxLayout(
            MDTopAppBar(title="Reinforcement Learning Presentation"),
            MDBoxLayout(
                MDCard(GridWorldView(config), padding="10dp"), padding="10dp"
            ),
            orientation="vertical",
        )
