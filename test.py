'''The test'''

import pytest
from app.src.business_logic.models import MenuItem, Drink, Dessert, Entree, Order
from app.src.business_logic.crud import Menu
import os
import tempfile

def test_menu_item_creation():
    item = MenuItem("Test Item", 9.99, "Test description", "test.jpg", 500)
    assert item.name == "Test Item"
    assert item.price == pytest.approx(9.99)
    assert item.description == "Test description"
    assert item.image_path == "test.jpg"
    assert item.calories == 500

def test_menu_item_validation():
    # Test invalid price
    with pytest.raises(ValueError):
        MenuItem("Test", -1.0, "desc", "img.jpg", 100)
    
    # Test invalid calories
    with pytest.raises(ValueError):
        MenuItem("Test", 1.0, "desc", "img.jpg", -100)
    
    # Test empty name
    with pytest.raises(ValueError):
        MenuItem("", 1.0, "desc", "img.jpg", 100)

def test_drink_creation():
    drink = Drink("Coke", 2.99, "Refreshing cola", 16, 150, "coke.jpg")
    assert drink.name == "Coke"
    assert drink.price == pytest.approx(2.99)
    assert drink.description == "Refreshing cola"
    assert drink.size == 16
    assert drink.calories == 150
    assert drink.image_path == "coke.jpg"
    assert str(drink) == "name: Coke - size: 16oz - price: 2.99 - description: Refreshing cola - calories: 150"

def test_drink_size_validation():
    # Test invalid size
    with pytest.raises(ValueError):
        Drink("Coke", 2.99, "Cola", 4, 150, "coke.jpg")  # too small
    with pytest.raises(ValueError):
        Drink("Coke", 2.99, "Cola", 45, 150, "coke.jpg")  # too large
    with pytest.raises(ValueError):
        Drink("Coke", 2.99, "Cola", "not a number", 150, "coke.jpg")  # not a number

    # Test valid sizes
    valid_sizes = [8, 12, 16, 20, 24, 32, 40, 44]
    for size in valid_sizes:
        drink = Drink("Coke", 2.99, "Cola", size, 150, "coke.jpg")
        assert drink.size == size

def test_dessert_creation():
    dessert = Dessert("Chocolate Cake", 5.99, "Rich chocolate cake", 400, "cake.jpg")
    assert dessert.name == "Chocolate Cake"
    assert dessert.price == pytest.approx(5.99)
    assert dessert.description == "Rich chocolate cake"
    assert dessert.calories == 400
    assert dessert.image_path == "cake.jpg"
    assert str(dessert) == "name: Chocolate Cake - price: 5.99 - description: Rich chocolate cake - calories: 400"

def test_entree_creation():
    entree = Entree("Steak", 19.99, "Juicy ribeye", 800, "steak.jpg")
    assert entree.name == "Steak"
    assert entree.price == pytest.approx(19.99)
    assert entree.description == "Juicy ribeye"
    assert entree.calories == 800
    assert entree.image_path == "steak.jpg"
    assert str(entree) == "name: Steak - price: 19.99 - description: Juicy ribeye - calories: 800"

def test_order_operations():
    order = Order()
    assert len(order.items) == 0
    assert order.total == 0
    assert order.drink is None
    assert order.dessert is None
    assert order.entree is None
    
    # Test adding items
    drink = Drink("Coke", 2.99, "Refreshing cola", 16, 150, "coke.jpg")
    entree = Entree("Steak", 19.99, "Juicy ribeye", 800, "steak.jpg")
    dessert = Dessert("Cake", 5.99, "Chocolate cake", 400, "cake.jpg")
    
    order.add_item(drink)
    assert len(order.items) == 1
    assert order.total == pytest.approx(2.99)
    
    order.add_item(entree)
    assert len(order.items) == 2
    assert order.total == pytest.approx(22.98)
    
    order.add_item(dessert)
    assert len(order.items) == 3
    assert order.total == pytest.approx(28.97)
    
    # Test removing items
    order.remove_item(drink)
    assert len(order.items) == 2
    assert order.total == pytest.approx(25.98)
    
    # Test removing non-existent item
    with pytest.raises(ValueError):
        order.remove_item(drink)  # drink was already removed
    
    # Test string representation
    assert str(order) == f"items: {[entree, dessert]} - drink: None - dessert: None - entree: None - total: {25.98}"

def test_order_edge_cases():
    order = Order()
    
    # Test removing from empty order
    with pytest.raises(ValueError):
        order.remove_item(MenuItem("Test", 1.0, "desc", "img.jpg", 100))
    
    # Test adding None
    with pytest.raises(ValueError):
        order.add_item(None)
    
    # Test adding invalid item type
    with pytest.raises(ValueError):
        order.add_item("not a menu item")
    
    # Test adding same item multiple times
    drink = Drink("Coke", 2.99, "Cola", 16, 150, "coke.jpg")
    order.add_item(drink)
    order.add_item(drink)  # Should work and add it twice
    assert len(order.items) == 2
    assert order.total == pytest.approx(5.98)

def test_menu_item_inheritance():
    # Test that all menu items inherit from MenuItem
    drink = Drink("Coke", 2.99, "Cola", 16, 150, "coke.jpg")
    dessert = Dessert("Cake", 5.99, "Chocolate cake", 400, "cake.jpg")
    entree = Entree("Steak", 19.99, "Juicy ribeye", 800, "steak.jpg")
    
    assert isinstance(drink, MenuItem)
    assert isinstance(dessert, MenuItem)
    assert isinstance(entree, MenuItem)

def test_crud_operations():
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        crud = Menu(csv_path=temp_path)
        
        # Test create
        item = crud.create_item(
            item_type='Entree',
            name='Test Burger',
            price=9.99,
            description='Test burger',
            calories=500,
            image_path='burger.jpg'
        )
        assert item['name'] == 'Test Burger'
        assert float(item['price']) == pytest.approx(9.99)
        
        # Test read
        items = crud.read_items()
        assert len(items) == 1
        assert items[0]['name'] == 'Test Burger'
        
        # Test read specific item
        burger = crud.read_item('Test Burger')
        assert burger is not None
        assert burger['name'] == 'Test Burger'
        
        # Test update
        updated = crud.update_item('Test Burger', price=10.99)
        assert float(updated['price']) == pytest.approx(10.99)
        
        # Test delete
        assert crud.delete_item('Test Burger')
        assert len(crud.read_items()) == 0
        
        # Test validation
        with pytest.raises(ValueError):
            crud.create_item(
                item_type='InvalidType',
                name='Invalid',
                price=9.99,
                description='Test',
                calories=500,
                image_path='test.jpg'
            )
            
        # Test drink size validation
        with pytest.raises(ValueError):
            crud.create_item(
                item_type='Drink',
                name='Invalid Drink',
                price=2.99,
                description='Test',
                calories=100,
                image_path='test.jpg',
                size=4
            )
            
    finally:
        # Clean up
        os.unlink(temp_path)

def test_crud_model_conversion():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        crud = Menu(csv_path=temp_path)
        
        # Create test items
        crud.create_item(
            item_type='Drink',
            name='Coke',
            price=2.99,
            description='Cola',
            calories=150,
            image_path='coke.jpg',
            size=16
        )
        
        crud.create_item(
            item_type='Entree',
            name='Burger',
            price=9.99,
            description='Beef burger',
            calories=500,
            image_path='burger.jpg'
        )
        
        # Test model conversion
        models = crud.get_menu_models()
        assert len(models) == 2
        assert isinstance(models['Coke'], Drink)
        assert isinstance(models['Burger'], Entree)
        assert models['Coke'].size == 16
        assert float(models['Burger'].price) == pytest.approx(9.99)
        
    finally:
        os.unlink(temp_path) 