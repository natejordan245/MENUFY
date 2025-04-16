from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MenuFooter(BoxLayout):
    def __init__(self, button_text="View Order", **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.1
        self.add_widget(Button(text=button_text)) 