from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MenuHeader(BoxLayout):
    def __init__(self, title="Restaurant Menu", **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.1
        self.add_widget(Label(text=title)) 