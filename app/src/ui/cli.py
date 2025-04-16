import sys
from src.business_logic.crud import Menu
def print_menu():
    print("\n" + "="*50)
    print("MENU MANAGEMENT SYSTEM")
    print("="*50)
    print("\nAvailable Operations:")
    print("1. Create new item")
    print("2. Read all items")
    print("3. Read specific item")
    print("4. Delete item")
    print("5. Exit")
    print("\n" + "-"*50)
    print("Enter your choice (1-5): ", end="")

def get_item_details():
    print("\n" + "-"*50)
    print("Enter Item Details:")
    print("-"*50)
    item_type = input("Item type (Entree/Drink/Dessert/Appetizer): ").strip()
    name = input("Item name: ").strip()
    price = float(input("Price: "))
    description = input("Description: ").strip()
    calories = int(input("Calories: "))
    image_path = input("Image path: ").strip()
    
    size = None
    if item_type == "Drink":
        size = int(input("Size (8-44 oz): "))
    
    return {
        'item_type': item_type,
        'name': name,
        'price': price,
        'description': description,
        'calories': calories,
        'image_path': image_path,
        'size': size
    }

def main():
    my_menu = Menu()
    
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == "1":
            try:
                item_data = get_item_details()
                item = my_menu.create_item(**item_data)
                print("\n" + "="*50)
                print(f"Item created successfully: {item['name']}")
                print("="*50)
            except ValueError as e:
                print("\n" + "!"*50)
                print(f"Error: {e}")
                print("!"*50)
                
        elif choice == "2":
            items = my_menu.read_items()
            print("\n" + "="*50)
            if not items:
                print("No items found.")
            else:
                print("All Items:")
                for item in items:
                    print(f"- {item['name']} ({item['type']}): ${item['price']}")
            print("="*50)
                    
        elif choice == "3":
            name = input("\nEnter item name to search: ").strip()
            item = my_menu.read_item(name)
            print("\n" + "="*50)
            if item:
                print("Item found:")
                for key, value in item.items():
                    print(f"{key}: {value}")
            else:
                print("Item not found.")
            print("="*50)
                
        elif choice == "4":
            name = input("\nEnter item name to delete: ").strip()
            try:
                if my_menu.delete_item(name):
                    print("\n" + "="*50)
                    print(f"Item '{name}' deleted successfully.")
                    print("="*50)
            except ValueError as e:
                print("\n" + "!"*50)
                print(f"Error: {e}")
                print("!"*50)
                
        elif choice == "5":
            print("\n" + "="*50)
            print("Goodbye!")
            print("="*50)
            sys.exit(0)
            
        else:
            print("\n" + "!"*50)
            print("Invalid choice. Please try again.")
            print("!"*50)

if __name__ == "__main__":
    main() 