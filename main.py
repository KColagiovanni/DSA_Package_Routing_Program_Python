# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
from package_delivery import DeliverPackages
from hash_table import HashTable
from wgups_time import WgupsTime
from datetime import time

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
            wtime.check_input(lookup_time)

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

            print(f'loaded_trucks is: {loaded_trucks}')
            # Loop through the packages on each truck and find the package with the shortest distance from the hub, and from
            # one delivery address to the next.
            for truck_num in range(len(loaded_trucks)):

                print(f'from main.py loaded_trucks[truck_num] is: {loaded_trucks[truck_num]}')
                print(f'from main.py truck_num is: {truck_num}')
                # print(f'from main.py {}')
                truck_list = dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks[truck_num], truck_num, record_data)  # [O(n^2)]

            for truck in range(len(dp.delivery_data)):
                dp.update_package_delivery_status_and_print_output_for_all_packages(
                    dp.delivery_data[truck][0],
                    truck + 1,
                    dp.delivery_data[truck][1],
                    lookup_time,
                    package_id=None,
                    package_index=None,
                    single_package_lookup=False
                )

        # Case if user selects Option #2
        # Get info for a single package at a particular time -> O(n)
        elif user_input == '2':

            # ht = HashTable(TABLE_SIZE)

            package_id = input('Enter a valid package ID: ')
            lookup_time = input('Enter a time (HH:MM:SS): ')
            print(f'User entered package ID {package_id} at {lookup_time}')

            wtime.check_input(lookup_time)

            print()
            print(f'Showing package info for Package ID {package_id} at {lookup_time}:')

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

            for truck_num in range(len(loaded_trucks)):

                print(f'from main.py loaded_trucks[truck_num] is: {loaded_trucks[truck_num]}')
                print(f'from main.py truck_num is: {truck_num}')
                # print(f'from main.py {}')
                # truck_list = dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks[truck_num], truck_num, record_data)  # [O(n^2)]
                truck_list = dp.find_shortest_distance(ppd.get_distance_data(), loaded_trucks[truck_num], truck_num, record_data)  # [O(n^2)]

                # print(f'truck_list is: {truck_list}')

            print(f'Package Data is: {ppd.get_hash().lookup_item(int(package_id))[1]}')
            for truck in range(len(dp.delivery_data)):
                if int(package_id) in dp.delivery_data[truck][0]:
                    package_index = dp.delivery_data[truck][0].index(int(package_id))
                    print(f'package_index is: {package_index}')
                    print(f'Package_id {package_id} is on truck {truck + 1}')
                    truck_num = truck

            dp.update_package_delivery_status_and_print_output_for_all_packages(
                dp.delivery_data[truck_num][0],
                truck_num + 1,
                dp.delivery_data[truck_num][1],
                lookup_time,
                package_id=package_id,
                package_index=package_index,
                single_package_lookup=True
            )

        # This exits the program
        elif user_input.lower() == 'quit':
            exit()

        # Print Invalid Entry and quit the program
        else:
            print('Invalid entry! Please try again.')
            continue


if __name__ == '__main__':
    main()
