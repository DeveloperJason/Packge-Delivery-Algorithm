# Jason Philpy ID: 001467497

from menu import main_menu_prompt
from distance_calculator import sort_all_trucks


if __name__ == '__main__':

    # Loads the trucks with the proper packages and sorts them via greedy sort
    sort_all_trucks()

    # Launches the menu and prompts the user for input
    main_menu_prompt()
