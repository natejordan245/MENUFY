# Menu Management System

A Python-based menu management system that allows users to create, read, update, and delete menu items through a command-line interface.

## Project Structure

```
app/
├── src/
│   ├── business_logic/
│   │   ├── __init__.py
│   │   ├── crud.py      # CRUD operations for menu items
│   │   └── models.py    # Data models for menu items
│   └── ui/
│       ├── __init__.py
│       └── cli.py       # Command-line interface implementation
├── __init__.py
├── main.py              # Application entry point
└── items.csv           # Data storage file
```

## Requirements

- Python 3.x
- Dependencies:
  - pytest (for testing)
  - tkinter (for GUI components)
  - kivy (for GUI components)

## Module Descriptions

### Business Logic Layer (`app/src/business_logic/`)

- **crud.py**: Implements the core CRUD (Create, Read, Update, Delete) operations for menu items
  - `Menu` class: Handles all menu item operations
  - Supports different item types: Entree, Drink, Dessert, Appetizer
  - Manages data persistence using CSV files

- **models.py**: Defines the data models for menu items
  - Contains class definitions for different types of menu items
  - Implements validation and data structure

### User Interface Layer (`app/src/ui/`)

- **cli.py**: Command-line interface implementation
  - Provides interactive menu for users
  - Handles user input and displays menu items
  - Implements all CRUD operations through user-friendly prompts

## Features

- Create new menu items with details like name, price, description, calories, and image path
- View all menu items or search for specific items
- Update existing menu items
- Delete menu items
- Support for different item types with specific attributes (e.g., drink sizes)
- Data persistence using CSV files

## Usage

1. Run the application:
   ```bash
   python -m app.main
   ```

2. Follow the on-screen prompts to:
   - Create new menu items
   - View existing items
   - Update item details
   - Delete items
   - Exit the application

## Development

- The project follows a modular architecture separating business logic from user interface
- Uses CSV files for data persistence
- Implements proper error handling and input validation
- Supports future GUI implementation through tkinter and kivy

## Authors

- Nathan Jordan
- Brandon Whitesides

