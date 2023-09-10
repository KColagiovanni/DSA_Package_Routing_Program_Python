# Author: Kevin Colagiovanni
# Student ID: 011039990

# from packages import total_distance
import parse_package_data as ppd
import calulate_distance
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
            (hours, minutes, seconds) = display_time.split(':')
            convert_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            print(f'User entered package ID {package_id} at {convert_time}')
            print(ppd.get_hash().lookup_item(package_id))
            cont_or_quit = input('Press any key then enter to continue or type "quit" to quit')
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
            input_package_id = int(input('Enter a package ID: '))
            ppd.load_trucks(input_package_id, num_of_packages)

            # index = ppd.get_input_data()[input_package_id - 1]
            # # print(f'index[1] is: {index[1]}, index[0] is {index[0]}')
            #
            # distance_list = ppd.sync_csv_data()[index[1]]
            # # print(f'distance_list: {distance_list}')
            # # print(f'Distance List:Package ID(#{index[0]}) is: {distance_list.get("Package ID")}')
            # # print(f'Distance List:Index(#{index[0]}) is: {distance_list.get("Index")}')
            #
            # for package_num in range(1, len(distance_list.get('Package ID')) + 1):
            #     test_truck_1.append(distance_list.get('Package ID').get(package_num))
            # print(f'Truck 1 Packages: {test_truck_1}')
            # # print(f'Shortest distance index: [{index[0]}][{ppd.find_shortest_distance(distance_list.get("Index"))}]')
            #
            # # print(f'distance_data(index {distance_list.get("Index")}) is: {ppd.get_distance_data()[distance_list.get("Index")]}')
            # # print(f'Shortest distance[{distance_list.get("Index")}][{ppd.find_shortest_distance(ppd.get_distance_data()[distance_list.get("Index")])}]')
            # ppd.sync_csv_data()
            # # print(f'Index {ppd.find_shortest_distance(distance_list)} is {ppd.get_input_data()[ppd.find_shortest_distance(distance_list)][1]}')
            # # ppd.load_trucks(ppd.match_distance_files_to_package_id[], distance_list)
            # # print(f'Shortest distance is: {ppd.find_shortest_distance(distance_list)}')

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
