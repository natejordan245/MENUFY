from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label

class ItemForm(BoxLayout):
    def __init__(self, on_submit=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        self.on_submit = on_submit

        # Item type selector
        self.add_widget(Label(text='Item Type:'))
        self.type_spinner = Spinner(
            text='Select Type',
            values=('Entree', 'Drink', 'Dessert', 'Appetizer')
        )
        self.add_widget(self.type_spinner)

        # Name input
        self.add_widget(Label(text='Name:'))
        self.name_input = TextInput(multiline=False)
        self.add_widget(self.name_input)

        # Price input
        self.add_widget(Label(text='Price:'))
        self.price_input = TextInput(multiline=False, input_filter='float')
        self.add_widget(self.price_input)

        # Description input
        self.add_widget(Label(text='Description:'))
        self.desc_input = TextInput(multiline=True)
        self.add_widget(self.desc_input)

        # Calories input
        self.add_widget(Label(text='Calories:'))
        self.calories_input = TextInput(multiline=False, input_filter='int')
        self.add_widget(self.calories_input)

        # Image path input
        self.add_widget(Label(text='Image Path:'))
        self.image_input = TextInput(multiline=False)
        self.add_widget(self.image_input)

        # Size input (only for drinks)
        self.add_widget(Label(text='Size (for drinks):'))
        self.size_input = TextInput(multiline=False)
        self.add_widget(self.size_input)

        # Submit button
        self.submit_btn = Button(text='Submit', size_hint_y=0.1)
        self.submit_btn.bind(on_press=self._on_submit)
        self.add_widget(self.submit_btn)

    def _on_submit(self, instance):
        if self.on_submit:
            data = {
                'type': self.type_spinner.text,
                'name': self.name_input.text,
                'price': float(self.price_input.text),
                'description': self.desc_input.text,
                'calories': int(self.calories_input.text),
                'image_path': self.image_input.text,
                'size': self.size_input.text if self.type_spinner.text == 'Drink' else None
            }
            self.on_submit(data) 