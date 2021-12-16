from distance_calculator import get_package_status
from distance_calculator import get_total_distance
from truck_loader import pkg_hash_table
import datetime


# O(1) Runs the main menu prompt allowing user to pick between seeing the full distance,
# a particular package or all of the packages statuses
def main_menu_prompt():
    print('What would you like to do?')
    print('Enter \'distance\' to see total miles the trucks drove')
    print('Enter a package ID')
    print('Enter \'all\' to see all package statuses')
    input_menu_choice = str(input('Enter \'exit\' to quit  \n'))
    if input_menu_choice.lower() == 'exit':
        exit()
    elif input_menu_choice.lower() == 'distance':
        print("Total distance by all trucks: " + str(get_total_distance()) + " miles \n")
        main_menu_prompt()
    else:
        if validate_pkg_input(input_menu_choice):
            pkg_id = 0
            if input_menu_choice.lower() != 'all':
                pkg_id = int(input_menu_choice)
            input_time = input('Enter a time in \'HH:MM:SS\' format: ')
            (hrs, mins, secs) = input_time.split(':')
            convert_user_time = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
            get_package_status(pkg_id, convert_user_time)
            main_menu_prompt()
        else:
            print('Not a valid package ID or command. \n')
            main_menu_prompt()


# Validates the input to make sure it is either the word all or a package ID that exists in the package table
def validate_pkg_input(menu_input):
    if menu_input.lower() == 'all':
        return True
    elif menu_input.isdigit():
        pkg_id = int(menu_input)
        return pkg_hash_table.look_up(pkg_id) is not None
    else:
        return False
