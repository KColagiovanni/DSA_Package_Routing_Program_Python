# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
from package_delivery import DeliverPackages
from wgups_time import WgupsTime

TABLE_SIZE = 40
NUMBER_OF_TRUCKS = 3
INVALID_ENTRY = 'Invalid Entry!'


def main():
    """
    This is the main function that runs the program. It asks for user input and executes code based on what the user
    enters.

    Time Complexity: O(n^2)

    Parameters: None

    Returns: None
    """
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

        user_input = input("""\nSelect one of the below options:
    Press 1 to display package info and status' for all packages at a specified time.
    Press 2 to display package info and status for a specific package at a specific time.
    Type 'quit' at any time to quit the program.
    
Selection: """)

        wtime = WgupsTime()

        # User enters 1
        if user_input == '1':

            lookup_time = input('Enter a time (HH:MM): ')

            # User wants to quit the program
            if lookup_time.lower() == 'quit':
                exit()

            wtime.check_input(lookup_time)  # [O(1)]

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
                    if ppd.get_hash().lookup_item(package_id)[1][0] != package_id:
                        print('That is not a valid Package ID.\n')
                    else:
                        break

            lookup_time = input('Enter a time (HH:MM:SS): ')

            # User wants to quit the program
            if lookup_time.lower() == 'quit':
                exit()

            wtime.check_input(lookup_time)  # [O(1)]

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

        # User entered invalid data.
        else:
            print('\nInvalid entry! Please try again.')
            continue


# Call the main function
if __name__ == '__main__':
    main()
