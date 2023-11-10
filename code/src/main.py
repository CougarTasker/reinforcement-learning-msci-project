from kivy.app import App
from kivy.uix.label import Label


class ReinforcementLearningApp(App):
    def build(self):
        return Label(text="Hello world")


def main():
    ReinforcementLearningApp().run()


if __name__ == "__main__":
    main()
