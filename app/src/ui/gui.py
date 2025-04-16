from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import traceback
from src.gui.components import MenuHeader, MenuScrollView, MenuFooter, ItemForm
from app.src.business_logic.crud import MenuCRUD

class MenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.crud = MenuCRUD()
        
        # Add components
        self.add_widget(MenuHeader())
        self.menu_scroll = MenuScrollView()
        self.add_widget(self.menu_scroll)
        
        # Add CRUD buttons
        button_box = BoxLayout(size_hint_y=0.1)
        add_btn = Button(text='Add Item')
        add_btn.bind(on_press=self.show_add_form)
        button_box.add_widget(add_btn)
        
        delete_btn = Button(text='Delete Item')
        delete_btn.bind(on_press=self.show_delete_dialog)
        button_box.add_widget(delete_btn)
        
        self.add_widget(button_box)
        self.add_widget(MenuFooter())

    def show_add_form(self, instance):
        form = ItemForm(on_submit=self.add_item)
        popup = Popup(title='Add Menu Item', content=form, size_hint=(0.8, 0.8))
        form.submit_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def add_item(self, data):
        try:
            self.crud.create_item(**data)
            self.refresh_menu()
        except Exception as e:
            self.show_error(str(e))

    def show_delete_dialog(self, instance):
        content = BoxLayout(orientation='vertical')
        name_input = TextInput(hint_text='Enter item name to delete')
        content.add_widget(name_input)
        
        btn = Button(text='Delete')
        btn.bind(on_press=lambda x: self.delete_item(name_input.text))
        content.add_widget(btn)
        
        popup = Popup(title='Delete Item', content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def delete_item(self, name):
        try:
            self.crud.delete_item(name)
            self.refresh_menu()
        except Exception as e:
            self.show_error(str(e))

    def refresh_menu(self):
        items = self.crud.read_items()
        self.menu_scroll.clear_widgets()
        for item in items:
            btn = Button(text=f"{item['name']} - ${item['price']}", size_hint_y=None, height=40)
            self.menu_scroll.add_widget(btn)

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class RestaurantApp(App):
    def build(self):
        Window.size = (400, 600)
        return MenuScreen()

def main():
    try:
        RestaurantApp().run()
    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:")
        print(traceback.format_exc())
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
