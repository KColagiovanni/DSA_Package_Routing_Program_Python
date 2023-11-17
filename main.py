# Student ID: 011039990
# Author: Kevin Colagiovanni

import hash_table
import package_delivery
import parse_package_data
import wgups_time
from parse_package_data import Packages
from package_delivery import DeliverPackages
from wgups_time import WgupsTime


def main():
    """
    This is the main function that runs the program. It asks for user input and executes code based on what the user
    enters.

    Time Complexity: O(n^2)

    Parameters: None

    Returns: None
    """
    print('\n\n           +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('           +                                                                     +')
    print('           +   ++           ++     ++++++     ++      ++  +++++++      +++++     +')
    print('           +   ++           ++   ++      ++   ++      ++  ++     ++  ++     ++   +')
    print('           +   ++     +     ++  ++            ++      ++  ++     ++   +++        +')
    print('           +    ++   +++   ++   ++     +++++  ++      ++  +++++++         +++    +')
    print('           +     ++ ++ ++ ++     ++      ++    ++    ++   ++         ++     ++   +')
    print('           +      +++   +++        ++++++        ++++     ++           +++++     +')
    print('           +                                                                     +')
    print('           +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    while True:

        print()
        print('<>' * 20 + ' Main Menu ' + '<>' * 20)
        user_input = input("""
Select one of the below options:
    Press 1 to display package info and status' for all packages at a specified time.
    Press 2 to display package info and status for a specific package at a specific time.
    Type 'doc' so see documentation.
    Type 'quit' at any time to quit the program.
    
Selection: """)

        wtime = WgupsTime()

        # User enters 1
        if user_input == '1':

            # Validate lookup time entry
            while True:
                lookup_time = input('Enter a time (HH:MM): ')

                try:
                    wtime.check_input(lookup_time)  # [O(1)]

                except ValueError as e:
                    print(f'{e}\n')
                    continue

                else:
                    break

            # User wants to quit the program
            if lookup_time.lower() == 'quit':
                exit()

            ppd = Packages()
            dp = DeliverPackages()
            record_data = {}
            number_of_packages = len(ppd.get_package_data())

            # Define the record data dictionary.
            for package_key in range(1, number_of_packages + 1):  # [O(n)]
                package = ppd.get_hash().lookup_item(package_key)
                record_data = ppd.sync_csv_data(package)

            # Manually load the trucks.
            loaded_trucks = dp.manual_load(record_data)  # [O(n^2)]

            # Loop through the packages on each truck and find the package with the shortest distance from the hub, and
            # from one delivery address to the next.
            for truck_num in range(len(loaded_trucks)):  # [O(n^2)]
                dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks[truck_num], truck_num, record_data)

            # Update and print out package data to the console.
            for truck in range(len(dp.delivery_data)):  # [O(n^2)]
                dp.update_package_delivery_status_and_print_output(
                    dp.delivery_data[truck][0],
                    truck + 1,
                    dp.delivery_data[truck][1],
                    lookup_time,
                    package_id=None,
                    package_index=None,
                    single_package_lookup=False
                )  # [O(n)]

        # User enters 2
        elif user_input == '2':

            ppd = Packages()
            dp = DeliverPackages()
            record_data = {}
            number_of_packages = len(ppd.get_package_data())

            # Validate Package ID entry.
            while True:
                package_id = input('Enter a valid package ID: ')

                if package_id.lower() == 'quit':
                    exit()

                if not package_id.isnumeric():
                    print('Please enter numerical values only for package ID.\n')
                else:
                    try:
                        check_input = ppd.get_hash().lookup_item(package_id)[1][0]
                    except IndexError:
                        print('That is not a valid Package ID.\n')
                        continue
                    else:
                        if check_input != package_id:
                            print('That is not a valid Package ID.\n')
                            continue
                        else:
                            break

            # Validate lookup time entry
            while True:
                lookup_time = input('Enter a time (HH:MM): ')

                try:
                    wtime.check_input(lookup_time)  # [O(1)]

                except ValueError as e:
                    print(f'{e}\n')
                    continue

                else:
                    break

            # User wants to quit the program
            if lookup_time.lower() == 'quit':
                exit()

            # Define the record data dictionary.
            for package_key in range(1, number_of_packages + 1):  # [O(n^2)]
                package = ppd.get_hash().lookup_item(package_key)
                record_data = ppd.sync_csv_data(package)

            # Manually load the trucks.
            loaded_trucks = dp.manual_load(record_data)  # [O(n^2)]

            # Loop through the packages on each truck and find the package with the shortest distance from the hub, and
            # from one delivery address to the next.
            for truck_num in range(len(loaded_trucks)):  # [O(n^2)]
                dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks[truck_num], truck_num, record_data)

            # Get info to update and print out package data to the console.
            for truck in range(len(dp.delivery_data)):  # [O(n^2)]
                if int(package_id) in dp.delivery_data[truck][0]:
                    package_index = dp.delivery_data[truck][0].index(int(package_id))
                    truck_num = truck

            # Update and print out package data to the console.
            dp.update_package_delivery_status_and_print_output(
                dp.delivery_data[truck_num][0],
                truck_num + 1,
                dp.delivery_data[truck_num][1],
                lookup_time,
                package_id=package_id,
                package_index=package_index,
                single_package_lookup=True
            )  # [O(n)]

        # User wants to quit the program
        elif user_input.lower() == 'quit':
            exit()

        # User wants to quit the program
        elif user_input.lower() == 'doc':
            while True:
                print()
                print('<>' * 17 + ' Documentation Menu ' + '<>' * 18)
                doc_selection = input('''
Select a Module to display it\'s documentation:
    1. main.py
    2. DeliverPackages class in package_delivery.py
    3. HashTable class in hash_table.py
    4. ParseCsvData class in parse_package_data.py
    5. Packages class in parse_package_data.py
    6. WgupsTime class in wgups_time.py
    
    Note: Press 'H' when viewing documentation so see a help menu.
    
    Enter 'back' to go back to the main menu or 'quit' to quit the program.

Selection: ''')

                if doc_selection == '1':
                    help(main.__name__)
                elif doc_selection == '2':
                    help(package_delivery.DeliverPackages)
                elif doc_selection == '3':
                    help(hash_table.HashTable)
                elif doc_selection == '4':
                    help(parse_package_data.ParseCsvData)
                elif doc_selection == '5':
                    help(parse_package_data.Packages)
                elif doc_selection == '6':
                    help(wgups_time.WgupsTime)
                elif doc_selection.lower() == 'back':
                    break
                elif doc_selection.lower() == 'quit':
                    quit()
                else:
                    print('Invalid entry.')
                    continue

        # User entered invalid data.
        else:
            print('\nInvalid entry! Please try again.')
            continue


# Call the main function
if __name__ == '__main__':
    main()
