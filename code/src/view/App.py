from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar.toolbar import MDTopAppBar

from . import primary_palette
from .GridWorldView import GridWorldView


class ReinforcementLearningApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = primary_palette

        return MDBoxLayout(
            MDTopAppBar(title="Reinforcement Learning Presentation"),
            MDBoxLayout(
                MDCard(GridWorldView(), padding="10dp"), padding="10dp"
            ),
            orientation="vertical",
        )
