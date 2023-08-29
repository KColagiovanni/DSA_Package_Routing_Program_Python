# Author: Kevin Colagiovanni
# Student ID: 011039990

# from packages import total_distance
from parse_package_data import get_hash, get_input_data, get_distance_data
import calulate_distance
import datetime

class Main:
    # This is the display message that is shown when the user runs the program. The interface is accessible from here
    # print('<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>')
    # print(' WGUPS Routing Program (C950 ~ DSA2) ')
    # print('<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>~<*>\n')

    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  ')
    print('+       _           _    ____   _     _  ___     ___          +  ')
    print('+       |            |  /    \  |     | |   \   /   \         +  ')
    print('+        \\    /\    /  |   ___  |     | | D  |  \___          + ')
    print('+         \\  /  \  /   |     |  |     | |___/       \         + ')
    print('+          \\/    \/     \____/   \___/  |       \___/         + ')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')


    while True:

        user_input = input("""
    Select one of the below options or type 'quit' to quit:
        Press 1 to enter a time to display info for all packages
        Press 2 to enter a package id and time to display info for a specific package
    """)

        if user_input == '1':
            display_time = input('Enter a time (HH:MM:SS): ')
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'Time entered is: {convert_time}')
            cont_or_quit = input('Press any key then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        # Case if user selects Option #2
        # Get info for a single package at a particular time -> O(n)
        elif user_input == '2':
            package_id = input('Enter a valid package ID: ')
            display_time = input('Enter a time (HH:MM:SS): ')
            print(f'User entered package ID {package_id} at {display_time}')
            print(get_hash().lookup_item(package_id))
            cont_or_quit = input('Press any key then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '3':
            print(get_distance_data()[int(get_input_data()[1])])
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '4':
            get_hash().create_key(40)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # Case 'exit'
        # This exits the program
        elif user_input == 'quit':
            exit()

        # Case Error
        # Print Invalid Entry and quit the program
        else:
            print('Invalid entry! Please try again.')
            continue
