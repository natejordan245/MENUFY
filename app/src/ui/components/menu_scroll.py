from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class MenuScrollView(ScrollView):
    def __init__(self, categories=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.8)
        
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        if categories is None:
            categories = ['Entrees', 'Drinks', 'Desserts']
            
        for cat in categories:
            btn = Button(text=cat, size_hint_y=None, height=40)
            grid.add_widget(btn)
            
        self.add_widget(grid) 