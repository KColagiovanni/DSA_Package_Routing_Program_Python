# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
import datetime


class Main:
    # This is the display message that is shown when the user runs the program. The interface is accessible from here
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+                                                                     +')
    print('+   ++           ++     ++++++     ++      ++  +++++++      +++++     +')
    print('+   ++           ++   ++      ++   ++      ++  ++     ++  ++     ++   +')
    print('+   ++     +     ++  ++            ++      ++  ++     ++   +++        +')
    print('+    ++   +++   ++   ++     +++++  ++      ++  +++++++         +++    +')
    print('+     ++ ++ ++ ++     ++      ++    ++    ++   ++         ++     ++   +')
    print('+      +++   +++        ++++++        ++++     ++           +++++     +')
    print('+                                                                     +')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    ppd = Packages()

    while True:

        user_input = input("""\nSelect one of the below options or type 'quit' to quit the program:
    Press 1 to enter a time to display info for all packages
    Press 2 to enter a package id and time to display info for a specific package

Selection: """)

        if user_input == '1':
            display_time = input('Enter a time (HH:MM:SS): ')
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'Time entered is: {convert_time}')
            cont_or_quit = input('Press any key, then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        # Case if user selects Option #2
        # Get info for a single package at a particular time -> O(n)
        elif user_input == '2':
            package_id = input('Enter a valid package ID: ')
            display_time = input('Enter a time (HH:MM:SS): ')
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'User entered package ID {package_id} at {convert_time}')
            print(ppd.get_hash().lookup_item(package_id))
            cont_or_quit = input('Press any key, then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '3':
            print(f'First Delivery: {ppd.get_hash().lookup_item(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '4':
            print(f'return from create_key() is: {ppd.get_hash().create_key(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '5':
            while True:
                input_package_id = int(input(f'Enter a package ID(1 - {len(ppd.get_input_data())}): '))
                try:
                    print(f'sending {input_package_id} to load_trucks()')
                    ppd.load_trucks(input_package_id)
                except IndexError:
                    print('!!!!! Invalid Package ID !!!!!\n')
                    continue
                except ValueError:
                    print('!!!!! Invalid Package ID !!!!!\n')
                    continue
                else:
                    break
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '6':
            print(f'Sending {int(ppd.get_package_data(ppd.get_input_data())[1][1])} to load_trucks()')
            print(f'Starting program... {ppd.load_trucks(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # Case 'exit'
        # This exits the program
        elif user_input.lower() == 'quit':
            exit()

        # Case Error
        # Print Invalid Entry and quit the program
        else:
            print('Invalid entry! Please try again.')
            continue
