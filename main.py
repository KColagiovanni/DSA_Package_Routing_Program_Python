# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
from package_delivery import DeliverPackages
from hash_table import HashTable
from datetime import time
from wgups_time import WgupsTime

TABLE_SIZE = 40
NUMBER_OF_TRUCKS = 3
INVALID_ENTRY = 'Invalid Entry!'

def main():

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

        wtime = WgupsTime()
        if user_input == '1':

            lookup_time = input('Enter a time (HH:MM): ')
            print(f'lookup time is: {lookup_time}')
            time_check = wtime.check_input(lookup_time)

            # try:
            #     (lookup_hours, lookup_minutes, lookup_seconds) = lookup_time.split(':')
            # except ValueError:
            #     if len(lookup_time.split(':')) ==2:
            #         (lookup_hours, lookup_minutes) = lookup_time.split(':')
            #         lookup_seconds = '00'
            #     else:
            #         print(f'{INVALID_ENTRY} Please check format and try again.')
            #         continue
            #
            #
            #
            # try:
            #     lookup_time = time(hour=int(lookup_hours), minute=int(lookup_minutes), second=int(lookup_seconds))
            # except ValueError:
            #     if int(lookup_hours) < 0 or int(lookup_hours) > 23:
            #         print(f'{INVALID_ENTRY} Hour must be between 0 and 23!')
            #     if int(lookup_minutes) < 0 or int(lookup_minutes) > 59:
            #         print(f'{INVALID_ENTRY} Minutes must be between 0 and 59!')
            #     if int(lookup_seconds) < 0 or int(lookup_seconds) > 59:
            #         print(f'{INVALID_ENTRY} Seconds must be between 0 and 59!')
            #     continue
            #     # if int(lookup_hours) > 24:
            #     #     print('In')
            print()
            print(f'Showing package info for all packages and trucks at {lookup_time}:')

            ppd = Packages()
            dp = DeliverPackages()
            record_data = {}
            number_of_packages = len(ppd.get_package_data())

            # Define the record data dictionary O(n^2)
            for package_key in range(1, number_of_packages + 1):  # O(n)
                package = ppd.get_hash().lookup_item(package_key)  # O(1)
                record_data = ppd.sync_csv_data(package)  # O(n)

            # Manually load the trucks. Input: Package_data (sync_csv_data). Output: Manually loaded trucks.
            loaded_trucks = dp.manual_load(record_data)  # [O(n)]

            truck_list = dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks, record_data)  # [O(n^2)]

            for truck in range(len(dp.delivery_data)):
                dp.update_package_delivery_status_and_print_output(
                    dp.delivery_data[truck][0], truck + 1, dp.delivery_data[truck][1], lookup_time
                )

        # Case if user selects Option #2
        # Get info for a single package at a particular time -> O(n)
        elif user_input == '2':

            ht = HashTable(TABLE_SIZE)

            package_id = input('Enter a valid package ID: ')
            display_time = input('Enter a time (HH:MM:SS): ')
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = time(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'User entered package ID {package_id} at {convert_time}')
            print(ht.lookup_item(package_id))
            cont_or_quit = input('Press any key, then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

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
