''' 
This module provides CRUD operations for the menu items.

The module defines a MenuCRUD class that provides methods for creating, reading, updating, and deleting menu items.

The class uses a CSV file to store the menu items.

Nathan Jordan and Brandon Whitesides
'''



import csv
from pathlib import Path
from . import models

class Menu:
    VALID_TYPES = ['Entree', 'Drink', 'Dessert', 'Appetizer']
    MIN_DRINK_SIZE = 8  # minimum size in ounces
    MAX_DRINK_SIZE = 44  # maximum size in ounces

    def __init__(self, csv_path='app/items.csv'):
        self.csv_path = csv_path
        self.items = self._load_items()

    def _load_items(self):
        """Load items from CSV file"""
        items = []
        if Path(self.csv_path).exists():
            with open(self.csv_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    items.append(row)
        return items

    def _save_items(self):
        """Save items to CSV file"""
        if not self.items:
            return
        
        fieldnames = self.items[0].keys()
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.items)

    def create_item(self, item_type, name, price, description, calories, image_path, size=None):
        """Create a new menu item"""
        # Validate item type
        if item_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid item type. Must be one of: {', '.join(self.VALID_TYPES)}")
        
        # Validate size for drinks
        if item_type == 'Drink':
            try:
                size = int(size)
                if not (self.MIN_DRINK_SIZE <= size <= self.MAX_DRINK_SIZE):
                    raise ValueError(f"Drink size must be between {self.MIN_DRINK_SIZE} and {self.MAX_DRINK_SIZE} ounces")
            except (ValueError, TypeError):
                raise ValueError(f"Drink size must be a number between {self.MIN_DRINK_SIZE} and {self.MAX_DRINK_SIZE} ounces")
        elif size is not None:
            raise ValueError("Size can only be specified for drinks")
        
        # Validate price
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            raise ValueError("Price must be a valid number")
        
        # Validate calories
        try:
            calories = int(calories)
            if calories <= 0:
                raise ValueError("Calories must be greater than 0")
        except ValueError:
            raise ValueError("Calories must be a valid integer")
        
        # Check for duplicate names
        if any(item['name'] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' already exists")
        
        new_item = {
            'type': item_type,
            'name': name,
            'price': str(price),
            'description': description,
            'calories': str(calories),
            'image_path': image_path,
            'size': str(size) if size is not None else None
        }
        
        self.items.append(new_item)
        self._save_items()
        return new_item

    def read_items(self):
        """Get all menu items"""
        return self.items

    def read_item(self, name):
        """Get a specific menu item by name"""
        for item in self.items:
            if item['name'] == name:
                return item
        return None

    def update_item(self, name, **kwargs):
        """Update a menu item"""
        for item in self.items:
            if item['name'] == name:
                # Validate type if being updated
                if 'item_type' in kwargs:
                    if kwargs['item_type'] not in self.VALID_TYPES:
                        raise ValueError(f"Invalid item type. Must be one of: {', '.join(self.VALID_TYPES)}")
                
                # Validate size if being updated
                if 'size' in kwargs:
                    if item['type'] == 'Drink':
                        try:
                            size = int(kwargs['size'])
                            if not (self.MIN_DRINK_SIZE <= size <= self.MAX_DRINK_SIZE):
                                raise ValueError(f"Drink size must be between {self.MIN_DRINK_SIZE} and {self.MAX_DRINK_SIZE} ounces")
                        except (ValueError, TypeError):
                            raise ValueError(f"Drink size must be a number between {self.MIN_DRINK_SIZE} and {self.MAX_DRINK_SIZE} ounces")
                    else:
                        raise ValueError("Size can only be specified for drinks")
                
                # Update fields
                for key, value in kwargs.items():
                    if key in item:
                        item[key] = str(value) if isinstance(value, (int, float)) else value
                self._save_items()
                return item
        raise ValueError(f"Item with name '{name}' not found")

    def delete_item(self, name):
        """Delete a menu item"""
        for i, item in enumerate(self.items):
            if item['name'] == name:
                del self.items[i]
                self._save_items()
                return True
        raise ValueError(f"Item with name '{name}' not found")

    def get_menu_models(self):
        """Convert CSV items to model objects with O(n) complexity"""
        menu_items = {}
        for item in self.items:
            try:
                menu_item = None
                if item['type'] == 'Drink':
                    menu_item = models.Drink(
                        name=item['name'],
                        price=float(item['price']),
                        description=item['description'],
                        size=int(item['size']),
                        calories=int(item['calories']),
                        image_path=item['image_path']
                    )
                elif item['type'] == 'Entree':
                    menu_item = models.Entree(
                        name=item['name'],
                        price=float(item['price']),
                        description=item['description'],
                        calories=int(item['calories']),
                        image_path=item['image_path']
                    )
                elif item['type'] == 'Dessert':
                    menu_item = models.Dessert(
                        name=item['name'],
                        price=float(item['price']),
                        description=item['description'],
                        calories=int(item['calories']),
                        image_path=item['image_path']
                    )
                
                if menu_item:
                    menu_items[menu_item.name] = menu_item
            except (KeyError, ValueError) as e:
                print(f"Error processing item {item.get('name', 'unknown')}: {e}")
                continue
                
        return menu_items 