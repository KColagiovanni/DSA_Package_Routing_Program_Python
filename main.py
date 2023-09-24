# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
from hash_table import HashTable
import datetime


def main():
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

            ppd = Packages()
            ht = HashTable()

            package_id = input('Enter a valid package ID: ')
            display_time = input('Enter a time (HH:MM:SS): ')
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'User entered package ID {package_id} at {convert_time}')
            print(ht.lookup_item(package_id))
            cont_or_quit = input('Press any key, then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '3':
            ppd = Packages()
            ht = HashTable()
            print(f'First Delivery: {ht.lookup_item(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '4':
            ppd = Packages()
            ht = HashTable()
            print(f'return from create_key() is: {ht.create_key(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '5':
            ppd = Packages()
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

            ppd = Packages()
            ht = HashTable()

            minimum_hour = 25
            minimum_minute = 60
            first_package_id = 0

            number_of_packages = ppd.get_package_data(ppd.get_input_data())

            print(f'\nnumber_of_packages is: {number_of_packages}')

            # Determine which package has the highest priority
            for package_key in range(1, number_of_packages + 1):

                print(f'\npackage_key is: {package_key}')

                package = ppd.get_hash().lookup_item(package_key)  # O(1)

                # Get "delivery by" time hour and minute
                if package[1][2] != 'EOD' and package[1][7] == "None":
                    hour = int(package[1][2][0:package[1][2].find(':')])
                    minute = int(package[1][2][-5:-3])

                    # Determine the highest priority package based on the earliest "deliver by" time
                    if hour < minimum_hour and minute < minimum_minute:
                        minimum_hour = hour
                        minimum_minute = minute
                        first_package_id, first_package_delivery_by_time = package[0], package[1][5]

                print(f'package[0] is: {package[0]}')
                ppd.analyze_package_data(package[0])  # O(1)

                print(f'package is: {package}')
                matched_data = ppd.sync_csv_data(package)

            print(f'\nmatched_data is: {matched_data}')
            print(f'\nfirst_package_id is: {first_package_id}')

            # print(f'int(ppd.get_package_data(ppd.get_input_data())[1][1]) is {int(ppd.get_package_data(ppd.get_input_data())[1][1])}')
            # print(f'Sending {int(ppd.get_package_data(ppd.get_input_data())[1][1])} to load_trucks()')
            # print(f'Starting program... {ppd.load_trucks(int(ppd.get_package_data(ppd.get_input_data())[1][1]))}')
            print(f'Starting program... {ppd.load_trucks(first_package_id)}')
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


if __name__ == '__main__':
    main()
