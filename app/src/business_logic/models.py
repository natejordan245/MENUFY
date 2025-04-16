class MenuItem:
    def __init__(self, name:str, price:float, description:str, image_path:str, calories:int):
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if calories < 0:
            raise ValueError("Calories cannot be negative")
            
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path
        self.calories = calories

    def __str__(self):
        return f"name: {self.name} - price: {self.price:.2f} - description: {self.description} - calories: {self.calories}"

class Drink(MenuItem):
    MIN_SIZE = 8  # minimum size in ounces
    MAX_SIZE = 44  # maximum size in ounces
    
    def __init__(self, name:str, price:float, description:str, size:int, calories:int, image_path:str):
        try:
            size = int(size)
        except (ValueError, TypeError):
            raise ValueError("Size must be an integer")
            
        if not (self.MIN_SIZE <= size <= self.MAX_SIZE):
            raise ValueError(f"Size must be between {self.MIN_SIZE} and {self.MAX_SIZE} ounces")
            
        super().__init__(name, price, description, image_path, calories)
        self.size = size

    def __str__(self):
        return f"name: {self.name} - size: {self.size}oz - price: {self.price:.2f} - description: {self.description} - calories: {self.calories}"

class Dessert(MenuItem):
    def __init__(self, name:str, price:float, description:str, calories:int, image_path:str):
        super().__init__(name, price, description, image_path, calories)

    def __str__(self):
        return f"name: {self.name} - price: {self.price} - description: {self.description} - calories: {self.calories}"

class Entree(MenuItem):
    def __init__(self, name:str, price:float, description:str, calories:int, image_path:str):
        super().__init__(name, price, description, image_path, calories)

    def __str__(self):
        return f"name: {self.name} - price: {self.price} - description: {self.description} - calories: {self.calories}"

class Appetizer(MenuItem):
    def __init__(self, name:str, price:float, description:str, calories:int, image_path:str):
        super().__init__(name, price, description, image_path, calories)

    def __str__(self):
        return f"name: {self.name} - price: {self.price} - description: {self.description} - calories: {self.calories}"

class Order:
    def __init__(self):
        self.items = []
        self.drink = None
        self.dessert = None 
        self.entree = None
        self.total = 0

    def add_item(self, item):
        if item is None:
            raise ValueError("Cannot add None as an item")
        if not isinstance(item, MenuItem):
            raise ValueError("Can only add MenuItem objects to order")
            
        self.items.append(item)
        self.total += item.price

    def remove_item(self, item):
        if not self.items:
            raise ValueError("Cannot remove item from empty order")
        if item not in self.items:
            raise ValueError("Item not found in order")
            
        self.items.remove(item)
        self.total -= item.price

    def __str__(self):
        return f"items: {self.items} - drink: {self.drink} - dessert: {self.dessert} - entree: {self.entree} - total: {self.total:.2f}"

