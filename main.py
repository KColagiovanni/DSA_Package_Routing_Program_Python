# Author: Kevin Colagiovanni
# Student ID: 011039990

from parse_package_data import Packages
from package_delivery import DeliverPackages
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
            lookup_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'Showing Package info for {lookup_time}')

            ppd = Packages()
            dp = DeliverPackages()

            minimum_hour = 25
            minimum_minute = 60
            first_package_id = 0

            number_of_packages = len(ppd.get_package_data())

            # Determine which package has the highest priority O(n^2)
            for package_key in range(1, number_of_packages + 1):  # O(n)

                package = ppd.get_hash().lookup_item(package_key)  # O(1)
                ppd.sync_csv_data(package)  # O(n)
                dp.analyze_package_data(package[0])  # O(1)

                # Get "delivery by" time hour and minute
                if package[1][2] != 'EOD' and package[1][7] == "None":
                    hour = int(package[1][2][0:package[1][2].find(':')])
                    minute = int(package[1][2][-5:-3])

                    # Determine the highest priority package based on the earliest "deliver by" time
                    if hour < minimum_hour and minute < minimum_minute:
                        minimum_hour = hour
                        minimum_minute = minute
                        first_package_id, first_package_delivery_by_time = package[0], package[1][5]

            dp.load_trucks(first_package_id, ppd.record)  # O(n^2)

            # for package_key in range(1, number_of_packages + 1):  # O(n)
            #     (hours, minutes, seconds) = dp.first_truck_delivery_times[package_key].split(':')
            #     ftd_times = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            #
            #     if ftd_times > lookup_time:
            #         print('been delivered')

            cont_or_quit = input('Press any key, then enter to continue or type "quit" to quit')
            if cont_or_quit != 'quit':
                continue
            else:
                break

        # Case if user selects Option #2
        # Get info for a single package at a particular time -> O(n)
        elif user_input == '2':

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
            print(f'First Delivery: {ht.lookup_item(int(ppd.get_package_data()[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '4':
            ppd = Packages()
            ht = HashTable()
            print(f'return from create_key() is: {ht.create_key(int(ppd.get_package_data()[1][1]))}')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # ~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        elif user_input == '5':

            ppd = Packages()
            dp = DeliverPackages()

            while True:
                input_package_id = int(input(f'Enter a package ID(1 - {len(ppd.get_input_data())}): '))
                try:
                    print(f'sending {input_package_id} to load_trucks()')
                    dp.load_trucks(input_package_id)
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
            dp = DeliverPackages()

            minimum_hour = 25
            minimum_minute = 60
            first_package_id = 0

            number_of_packages = len(ppd.get_package_data())

            # Determine which package has the highest priority O(n^2)
            for package_key in range(1, number_of_packages + 1):  # O(n)

                package = ppd.get_hash().lookup_item(package_key)  # O(1)
                ppd.sync_csv_data(package)  # O(n)
                dp.analyze_package_data(package[0])  # O(1)

                # Get "delivery by" time hour and minute
                if package[1][2] != 'EOD' and package[1][7] == "None":
                    hour = int(package[1][2][0:package[1][2].find(':')])
                    minute = int(package[1][2][-5:-3])

                    # Determine the highest priority package based on the earliest "deliver by" time
                    if hour < minimum_hour and minute < minimum_minute:
                        minimum_hour = hour
                        minimum_minute = minute
                        first_package_id, first_package_delivery_by_time = package[0], package[1][5]

            dp.load_trucks(first_package_id, ppd.record)  # O(n^2)

            # ppd.get_hash().update_item(first_package_id, 6, 'En Route')
            # print(ppd.get_hash().lookup_item(first_package_id))
            # ppd.get_hash().update_item(first_package_id, 1, '4167 Converse St')
            # print(ppd.get_hash().lookup_item(first_package_id))
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
