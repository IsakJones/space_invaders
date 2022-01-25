""" 
DOCSTRING
    
This file contains the main function, which creates a Menu object.
The Menu object handles all control flow and game logic.
""" 

from src.menu import Menu

def main():
    """
    Creates menu object and calls function for main menu.
    """
    menu = Menu()
    menu.start()

if __name__ == "__main__":
    main()