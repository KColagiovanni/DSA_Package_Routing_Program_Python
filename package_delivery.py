from parse_package_data import Packages
from hash_table import HashTable
from wgups_time import WgupsTime
import datetime
from datetime import time

ppd = Packages()
ht = HashTable()
wtime = WgupsTime()

DELIVERY_TRUCK_SPEED_MPH = 18
MAX_PACKAGES_PER_TRUCK = 16
FIRST_TRUCK_DEPARTURE_TIME = '8:00:00'
MAX_TRUCKS_TRAVEL_DISTANCE = 140


class DeliverPackages:

    def __init__(self):

        self.first_truck = []
        self.first_truck_delivery_times = []
        self.total_dist_first_truck = []

        self.second_truck = []
        self.second_truck_delivery_times = []
        self.total_dist_second_truck = []

        self.third_truck = []
        self.third_truck_delivery_times = []
        self.total_dist_third_truck = []

        self.been_loaded = []
        self.addresses = [0]
        self.distance_traveled = []
        self.delivery_data = []
        self.total_distance_traveled = []
        self.total_delivery_time = []

        self.packages_to_be_delivered_together = set(())
        self.high_priority_packages = {}
        self.delivery_status = {}

        self.second_truck_departure_time = ''
        self.total_packages_loaded = 0
        self.high_priority_count = 0

    # Analyze the special notes and deliver by times and add packages to trucks as needed - [O(1)]
    def manual_load(self, record_data):

        print(f'record_data is: {record_data}')
        # print(f'ppd.record is: {ppd.record}')

        # Get Truck
        for record in record_data:

            truck = record_data[record].get('Truck')

            if truck is None:
                print('No Truck Data')
            else:
                if truck == 1:
                    print('Truck 1')
                if truck == 2:
                    print('Truck 2')
                if truck == 3:
                    print('Truck 3')

        # Get Delivery By Time
        for record in record_data:

            deliver_by_time = record_data[record].get('Deliver By')

            if deliver_by_time is None:
                print('No deliver by time')
            else:
                print(f'deliver_by_time is: {deliver_by_time}')

        # Delayed Package
        for record in record_data:

            delayed_package = record_data[record].get('Delayed ETA')

            if delayed_package is None:
                print('Package is not delayed')
            else:
                print(f'Delayed package ETA: {delayed_package}')

        # Packages going to the same address
        for record in record_data:

            deliver_together = record_data[record].get('Package ID')

            if deliver_together is None:
                print('No Package Data')
            else:
                if len(deliver_together) == 1:
                    print(f'Solo package: {deliver_together[1]}')
                else:
                    print('Packages going to the same address:')
                    for package_num in deliver_together:
                        print(f'\t\t\t{deliver_together[package_num]}')

        # Must be on the same truck
        for record in record_data:

            deliver_together = record_data[record].get('Deliver Together')

            if deliver_together is None:
                print('No delivery grouping required')
            else:
                print(deliver_together)

        # package_data = ppd.get_hash().lookup_item(key)  # O(1)

        # print(f'record_data is: {record_data}')

        # if 'Can only be on truck' in package_data[1][7] or 'Must be delivered with' in package_data[1][7] or 'Delayed' in package_data[1][7] or package_data[1][2] != 'EOD':
        #     self.high_priority_packages.update({package_data[0]: {}})

        # # Get packages that need to be delivered together on the same truck
        # if 'Must be delivered with' in package_data[1][7]:
        #     self.packages_to_be_delivered_together.add(package_data[0])
        #     package1 = int(package_data[1][7][-7:-5])
        #     self.packages_to_be_delivered_together.add(package1)
        #     package2 = int(package_data[1][7][-2:])
        #     self.packages_to_be_delivered_together.add(package2)
        #
        #     # self.high_priority_packages[package_data[0]]['Deliver Together'] = self.packages_to_be_delivered_together
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #
        # # Loading packages into the specific trucks that special instructions request.
        # if 'Can only be on truck' in package_data[1][7]:
        #
        #     # For truck 1
        #     if package_data[1][7][-1] == '1':
        #         if int(package_data[0]) not in self.first_truck:
        #             self.first_truck.append(int(package_data[0]))
        #             self.been_loaded.append(int(package_data[0]))
        #             self.total_packages_loaded += 1
        #             # self.high_priority_packages[package_data[0]].update({'Truck': 1})
        #
        #     # For truck 2
        #     elif package_data[1][7][-1] == '2':
        #         if int(package_data[0]) not in self.second_truck:
        #             self.second_truck.append(int(package_data[0]))
        #             self.been_loaded.append(int(package_data[0]))
        #             self.total_packages_loaded += 1
        #             # self.high_priority_packages[package_data[0]].update({'Truck': 2})
        #
        #     # For truck 3
        #     elif package_data[1][7][-1] == '3':
        #         if int(package_data[0]) not in self.third_truck:
        #             self.third_truck.append(int(package_data[0]))
        #             self.been_loaded.append(int(package_data[0]))
        #             self.total_packages_loaded += 1
        #             # self.high_priority_packages[package_data[0]].update({'Truck': 3})
        #
        # # Determine priority and load delayed packages on later trucks
        # if 'Delayed on flight' in package_data[1][7]:
        #     package_eta = package_data[1][7][-7:-3]
        #
        #     # self.high_priority_packages[package_data[0]].update({'Delayed ETA': self.convert_time(package_eta + ':00').strftime('%H:%M:%S')})
        #
        #     if package_data[1][2] != 'EOD':
        #         print(f'DELAYED | HIGH PRIORITY: {package_data[0]}'
        #         f'- ETA: {package_eta} (Deliver by: {package_data[1][2]})')
        #         self.second_truck.append(int(package_data[0]))
        #         self.high_priority_count += 0
        #         self.been_loaded.append(int(package_data[0]))
        #         self.total_packages_loaded += 1
        #         self.second_truck_departure_time = package_eta + ':00'
        #     else:
        #         print(f'DELAYED | {package_data[0]} - ETA: {package_eta} (Deliver by: {package_data[1][2]})')
        #         self.third_truck.append(int(package_data[0]))
        #         self.been_loaded.append(int(package_data[0]))
        #         self.total_packages_loaded += 1
        #
        # # Get "delivery by" time hour and minute
        # if package_data[1][2] != 'EOD':# and package_data[1][7] == "None":
        #     hour = int(package_data[1][2][0:package_data[1][2].find(':')])
        #     minute = int(package_data[1][2][-5:-3])
        #
        #     # if len(package_data[1][0]) < 2:
        #     #     package_data[1][0] = '0' + package_data[1][0]
        #
        #     # self.high_priority_packages[package_data[0]].update({'Deliver By': self.convert_time(package_data[1][2]).strftime('%H:%M:%S')})
        #
        # # else:
        # #     self.high_priority_packages[package_data[0]].update({'Deliver By': package_data[1][2]})
        #     # self.high_priority_packages['Package ID'][package_data[0]]['Deliver By'] = f'{hour}:{minute}'
        #
        #     # if hour < 10 and minute <= 30:
        #     # self.first_truck.append(int(package_data[0]))
        #     self.second_truck.append(int(package_data[0]))
        #     self.been_loaded.append(int(package_data[0]))
        #     self.total_packages_loaded += 1
        #     # else:
        #     #     # self.second_truck.append(int(package_data[0]))
        #     #     self.been_loaded.append(int(package_data[0]))
        #     #     self.total_packages_loaded += 1
        #     #     self.second_truck.insert(self.high_priority_count, int(package_data[0]))
        #
        #
        # # print(f'\nHigh Priority Packages: {self.high_priority_packages}')
        #
        # # Loading packages into the specific trucks that special instructions request.
        # # if 'Can only be on truck' in package_data[1][7]:
        #
        #
        # print(f'\nTruck 1: {self.first_truck}')
        # print(f'Truck 2: {self.second_truck}')
        # print(f'Truck 3: {self.third_truck}')

    # Find shortest distance from and to the hub O(n)
    def find_shortest_distance_from_and_to_hub(self, distances, record_dict):

        shortest_index = 0
        min_dist = distances[1][0]

        for row in range(1, len(distances)):  # O(n)
            if float(distances[row][0]) < float(min_dist):
                min_dist = float(distances[row][0])
                shortest_index = row
                # print(f'shortest_distance is: {shortest_index}')

        return record_dict[ppd.get_distance_name_data()[shortest_index][2]]['Package ID'][1]

    # Returns the index of the shortest distance - [O(n^2)]
    def find_shortest_distance(self, distances, search_row_index):

        # Get index where the search will begin.
        if float(distances[search_row_index][1]) > 0:
            # print(f'from find_shortest_distance float(distances[{search_row_index}][1]) (start search index) is: {float(distances[search_row_index][1])}')
            min_dist = float(distances[search_row_index][1])
            t_direction = 'horizontal'
        else:
            # print(f'from find_shortest_distance float(distances[{search_row_index + 1}][1]) (start search index) is: {float(distances[search_row_index + 1][1])}')
            min_dist = float(distances[search_row_index + 1][1])
            t_direction = 'vertical'

        search_data = {
            'min_horizontal_index': 0,
            'min_vertical_index': 0,
            'traversal_direction': t_direction,
            'min_dist': min_dist,
            # 'min_dist': float(MAX_TRUCKS_TRAVEL_DISTANCE),
            'min_dist_location': 'horizontal'
        }

        # row_data = ppd.get_hash().lookup_item(<package id>)
        #
        # print(f'row_data is: {row_data}')

        ##### IF TRUCK IS EMPTY AND ABOUT TO START BEING PACKED, LOAD FIRST PACKAGE #####

        # print(f'distances[search_row_index][1] is: {distances[search_row_index][1]}')

        for row in range(1, len(distances[search_row_index])):  # O(n)

            ##### iF THE TRUCK IS FULLY PACKED MINUS 1 PACKAGE, CHECK SHORTEST DISTANCE BACK TO HUB #####
            if distances[search_row_index][row] == '0.0':
                search_data['traversal_direction'] = 'vertical'

            # if row in self.addresses:  # O(n) (in a for loop makes this O(n^2))
            #     # print(f'{row} is in {self.addresses}')
            #     continue

            if search_data['traversal_direction'] == 'horizontal':
                # print(f"\nsearch_data['traversal_direction'] is: {search_data['traversal_direction']}")
                if distances[search_row_index][row] != '':
                    # print(f"{float(distances[search_row_index][row])} < {search_data['min_dist']}({float(distances[search_row_index][row]) < search_data['min_dist']})")
                    if float(distances[search_row_index][row]) < search_data['min_dist']:
                        if float(distances[search_row_index][row]) != 0.0:
                            if search_row_index not in self.addresses:  # O(n) (in a for loop makes this O(n^2))
                                print(f'distances[{search_row_index}][{row}] is: {float(distances[search_row_index][row])}')
                                search_data['min_dist'] = float(distances[search_row_index][row])
                                # print(f"search_data['min_dist'] is: {search_data['min_dist']}")
                                search_data['min_dist_location'] = 'horizontal'
                                search_data['min_horizontal_index'] = row

            if search_data['traversal_direction'] == 'vertical':
                # print(f"\nsearch_data['traversal_direction'] is: {search_data['traversal_direction']}")
                if distances[row][search_row_index] != '':
                    # print(f"{float(distances[row][search_row_index])} < {search_data['min_dist']}({float(distances[row][search_row_index]) < search_data['min_dist']})")
                    if float(distances[row][search_row_index]) < search_data['min_dist']:
                        # print(f"{float(distances[row][search_row_index])} != 0.0 ({float(distances[row][search_row_index]) != 0.0})")
                        if float(distances[row][search_row_index]) != 0.0:
                            if row not in self.addresses:  # O(n) (in a for loop makes this O(n^2))
                                print(f'distances[{row}][{search_row_index}] is: {float(distances[row][search_row_index])}')
                                search_data['min_dist'] = float(distances[row][search_row_index])
                                # print(f"search_data['min_dist'] is: {search_data['min_dist']}")
                                search_data['min_dist_location'] = 'vertical'
                                search_data['min_vertical_index'] = row

            # print(f'distances[{search_row_index}][{row}] is: {distances[search_row_index][row]}')
            # print(f'distances[{row}][{search_row_index}] is: {distances[row][search_row_index]}')

        # print(f"from find_shortest_distance, search_data is: {search_data}")
        # print(f'Address indexes that have been added: {self.addresses}')

        self.distance_traveled.append(float(search_data["min_dist"]))
        # print(f'self.first_truck is: {self.first_truck}')
        # print(f'self.second_truck is: {self.second_truck}')
        # print(f'self.third_truck is: {self.third_truck}')
        # print(f'self.distance_traveled is: {self.distance_traveled}\n')

        # print(f'distance_traveled is: {self.distance_traveled}')

        if search_row_index not in self.addresses:  # O(n)
            self.addresses.append(search_row_index)

        if search_data["min_horizontal_index"] == 0 and search_data["min_vertical_index"] == 0:
            for index in range(1, len(distances[search_row_index])):  # O(n)
                if index not in self.addresses:  # O(n) (in a for loop makes this O(n^2))
                    search_data['min_horizontal_index'] = index
                    search_data['min_vertical_index'] = index

        if search_data['min_dist_location'] == 'horizontal':
            print(f"returning horizontal: {search_data['min_horizontal_index']}")
            return search_data['min_horizontal_index']
        if search_data['min_dist_location'] == 'vertical':
            print(f"returning vertical: {search_data['min_vertical_index']}")
            return search_data['min_vertical_index']

        # if search_row_index not in self.addresses:  # O(n)
        #     self.addresses.append(search_row_index)
        #
        # if search_data["min_horizontal_index"] == 0 and search_data["min_vertical_index"] == 0:
        #     for index in range(1, len(distances[search_row_index])):  # O(n)
        #         if index not in self.addresses:  # O(n) (in a for loop makes this O(n^2))
        #             print(f'index is(if): {index}')
        #             search_data['min_horizontal_index'] = index
        #             search_data['min_vertical_index'] = index
        #         else:
        #             print(f'self.addresses from shortest is: {self.addresses}')
        #             print(f'index is(else): {index}')
        #
        #
        # if search_data['min_dist_location'] == 'horizontal':
        #     print(f"returning horizontal: {search_data['min_horizontal_index']}")
        #     return search_data['min_horizontal_index']
        # if search_data['min_dist_location'] == 'vertical':
        #     print(f"returning vertical: {search_data['min_vertical_index']}")
        #     return search_data['min_vertical_index']


    # Check if a truck can be loaded more efficiently if it was initially loaded with
    # required packages prior to being loaded by the shortest distance method
    def maximize_efficiency(self, truck_list):

        for package_id in truck_list:

            package_id_data = ppd.get_input_data()[int(package_id) - 1]

            # Info from record dict/sync_csv_data(). Initially passed in from main.py.
            distance_list = ppd.record[ppd.get_hash().lookup_item(int(package_id_data[0]))[1][1]]  # [O(1)]

            print(f'from maximize_efficiency, distance_list is: {distance_list}')

    # Calculate the delivery distance between each package in the loaded truck - [O(n)]
    @staticmethod
    def calculate_truck_distance(package_list, delivery_info_dict):

        truck_distance_list = []

        #XXXXXXXXXX What about the find_shortest_distance_to_and_from hub method? XXXXXXXXXX#
        hub_to_first_delivery = float(ppd.get_distance_data()[int(
            delivery_info_dict.get(ppd.get_input_data()[package_list[0] - 1][1])["Index"]
        )][0])  # [O(1)]

        last_delivery_to_hub = float(ppd.get_distance_data()[int(
                delivery_info_dict.get(ppd.get_input_data()[package_list[-1] - 1][1])["Index"]
        )][0])  # [O(1)]

        # Distance from the hub to the first address.
        truck_distance_list.append(hub_to_first_delivery)

        # Iterate over
        for distance in range(1, len(package_list)):

            index1 = int(delivery_info_dict.get(ppd.get_input_data()[package_list[distance - 1] - 1][1])['Index'])
            index2 = int(delivery_info_dict.get(ppd.get_input_data()[package_list[distance] - 1][1])['Index'])

            if index1 > index2:
                indexes = [index1, index2]
            else:
                indexes = [index2, index1]

            truck_distance_list.append(float(ppd.get_distance_data()[indexes[0]][indexes[1]]))

        # Distance from the last address to the hub.
        truck_distance_list.append(float(last_delivery_to_hub))

        return round(sum(truck_distance_list), 2), truck_distance_list

    # Calculates the time it takes to go from one delivery to the next
    # and also the total delivery time for the truck - [O(n)]
    @staticmethod
    def calculate_delivery_time(package_distance_list, departure_time):

        (hours, minutes, seconds) = departure_time.split(':')
        converted_departure_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

        cumulative_delivery_duration_list = []
        delivery_time_list = []
        total_duration = 0

        for package_distance in package_distance_list:
            duration = round((package_distance / DELIVERY_TRUCK_SPEED_MPH), 2)
            total_duration += duration
            cumulative_delivery_duration_list.append(
                str(converted_departure_time + datetime.timedelta(hours=float(total_duration))))
            delivery_time_list.append(str(datetime.timedelta(hours=float(duration))))

        return delivery_time_list, cumulative_delivery_duration_list

    # Print verbose delivery data
    def print_verbose_output(self):

        # Output the result
        print()
        print('#' * 120)
        print(' ' * 45 + 'All packages have been loaded')
        print('#' * 120)

        print(f'\nTruck 1 Package IDs: {self.first_truck}(# of packages: {len(self.first_truck)},'
              f' Distance: {self.total_dist_first_truck[0]} miles)')
        print(f'Truck 1 Distance List: {self.total_dist_first_truck[1]}(miles)')
        print(f'Truck 1 Delivery Times: {self.first_truck_delivery_times[1]}')
        print(f'Truck 1 Duration Times: {self.first_truck_delivery_times[0]}')

        print(f'\nTruck 2 Package IDs: {self.second_truck}(# of packages: {len(self.second_truck)},'
              f' Distance: {self.total_dist_second_truck[0]} miles)')
        print(f'Truck 2 Distance List: {self.total_dist_second_truck[1]}(miles)')
        print(f'Truck 2 Delivery Times: {self.second_truck_delivery_times[1]}')
        print(f'Truck 2 Duration Times: {self.second_truck_delivery_times[0]}')

        print(f'\nTruck 3 Package IDs: {self.third_truck}(# of packages: {len(self.third_truck)},'
              f' Distance: {self.total_dist_third_truck[0]} miles)')
        print(f'Truck 3 Distance List: {self.total_dist_third_truck[1]}(miles)')
        print(f'Truck 3 Delivery Times: {self.third_truck_delivery_times[1]}')
        print(f'Truck 3 Duration Times: {self.third_truck_delivery_times[0]}')

        total_distance_traveled = round(
            self.total_dist_first_truck[0] +
            self.total_dist_second_truck[0] +
            self.total_dist_third_truck[0], 2
        )

        print(f'\nTotal Distance traveled: {total_distance_traveled} miles')
        print('#' * 120)

    # Loads packages onto the trucks, using recursion - [O(n^3)](find_shortest_distance(), which is called recursively
    # is O(n^2)).
    def load_trucks(self, package_id, delivery_info_dict):

        not_loaded = set()

        while self.total_packages_loaded < len(ppd.get_input_data()):
            print(f'# Loaded: {len(self.been_loaded)} | # of packages: {len(ppd.get_input_data())}')

            package_id_data = ppd.get_input_data()[int(package_id) - 1]

            # Info from record dict/sync_csv_data(). Initially passed in from main.py.
            distance_list = delivery_info_dict[ppd.get_hash().lookup_item(int(package_id_data[0]))[1][1]]  # [O(1)]

            # print(f'\npackage_id_data is: {package_id_data}')
            # print(f'distance_list is: {distance_list}')

        # if int(package_id) in self.high_priority_packages.keys():
        #     print(f'self.high_priority_packages[{package_id}] is: {self.high_priority_packages[int(package_id)]}')
        # else:
        #     print(f'No high priority data for package {package_id}')

        # if package_id in self.been_loaded:
        #     print(f'{package_id} has already been loaded.')
        #
        # else:

            # Load first Truck

            # Check if there is room for the package(s) that are going to a specific address on the truck. If there is
            # room for the package(s) to be loaded then has_room_bool will be True, if not it will be False.

            # Truck 1
            print(f"Truck 1: len(self.first_truck) + len(distance_list.get('Package ID')) is: {len(self.first_truck) + len(distance_list.get('Package ID'))}")
            if len(self.first_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
                has_room_bool1 = True
            else:
                has_room_bool1 = False

            # Truck 2
            print(f"Truck 2: len(self.second_truck) + len(distance_list.get('Package ID')) is: {len(self.second_truck) + len(distance_list.get('Package ID'))}")
            if len(self.second_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
                has_room_bool2 = True
            else:
                has_room_bool2 = False

            # Truck 3
            print(f"Truck 3: len(self.third_truck) + len(distance_list.get('Package ID')) is: {len(self.third_truck) + len(distance_list.get('Package ID'))}")
            if len(self.third_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
                has_room_bool3 = True
            else:
                has_room_bool3 = False

            # Check if there is a requirement for a specific package to be on a specific truck. If the specific package
            # needs to be on a specific truck, then load_on_truck_bool will be True, if not it will be False.

            # Truck 1
            truck_num = distance_list.get('Truck')
            load_on_truck1_bool = False
            if truck_num is not None:
                if truck_num == 1:
                    load_on_truck1_bool = True

            # Truck 2
            truck_num = distance_list.get('Truck')
            load_on_truck2_bool = False
            if truck_num is not None:
                if truck_num == 2:
                    load_on_truck2_bool = True

            # Truck 3
            truck_num = distance_list.get('Truck')
            load_on_truck3_bool = False
            if truck_num is not None:
                if truck_num == 3:
                    load_on_truck3_bool = True

            # Check if there is a specific delivery time that the package has to be delivered by. If so, the delivery
            # time that the package gets delivered based on the position it was loaded on the truck will be checked. If it is okay and the package will
            # be delivered on time or there is no specified deliver time, then deliver_by_bool will be True, if not it
            # will be False.

            # Truck 1
            deliver_by_time = distance_list.get('Deliver By')
            # deliver_by_bool1 = True
            # if deliver_by_time is not None:
                # print(f"distance_list['Package ID'].values() is: {distance_list['Package ID'].values()}")
            if deliver_by_time == 'EOD' and not load_on_truck1_bool:
                deliver_by_bool1 = False
            elif deliver_by_time == 'EOD' and load_on_truck1_bool:
                deliver_by_bool1 = True
            else:
                if len(self.first_truck) == 0:
                    if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                        deliver_by_bool1 = True
                    else:
                        deliver_by_bool1 = False
                else:
                    if wtime.time_difference(deliver_by_time, self.first_truck_delivery_times[1][-1]) > 0:
                        deliver_by_bool1 = True
                    else:
                        deliver_by_bool1 = False
            # else:
            #     deliver_by_bool1 = True

            # Truck 2
            deliver_by_time = distance_list.get('Deliver By')
            # deliver_by_bool2 = False
            # if deliver_by_time is not None:
            if deliver_by_time == 'EOD' and not load_on_truck2_bool:
                deliver_by_bool2 = False
                print(f'[457] - deliver_by_bool2 is: {deliver_by_bool2}')
            elif deliver_by_time == 'EOD' and load_on_truck2_bool:
                deliver_by_bool2 = True
                print(f'[460] - deliver_by_bool2 is: {deliver_by_bool2}')
            else:
                if len(self.second_truck) == 0:
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        deliver_by_bool2 = True
                        print(f'[465] - deliver_by_bool2 is: {deliver_by_bool2}')
                    else:
                        deliver_by_bool2 = False
                        print(f'[468] - deliver_by_bool2 is: {deliver_by_bool2}')
                else:
                    print(f'[470] - deliver_by_time is: {deliver_by_time}')
                    print(f'[471] - self.second_truck_delivery_times[1][-1] is: {self.second_truck_delivery_times[1][-1]}')
                    print(f'[472] - time difference is: {wtime.time_difference(deliver_by_time, self.second_truck_delivery_times[1][-1])}')
                    if wtime.time_difference(deliver_by_time, self.second_truck_delivery_times[1][-1]) > 0:
                        deliver_by_bool2 = True
                        print(f'[475] - deliver_by_bool2 is: {deliver_by_bool2}')
                    else:
                        deliver_by_bool2 = False
                        print(f'[478] - deliver_by_bool2 is: {deliver_by_bool2}')
            # else:
            #     deliver_by_bool2 = True

            # Truck 3
            deliver_by_time = distance_list.get('Deliver By')
            # deliver_by_bool3 = False
            # if deliver_by_time is not None:
            if deliver_by_time == 'EOD':
                deliver_by_bool3 = True
                print(f'[488] - deliver_by_bool3 is: {deliver_by_bool3}')
            else:
                if len(self.third_truck) == 0:
                    if len(self.first_truck) == 0:
                        deliver_by_bool3 = False
                        print(f'[493] - deliver_by_bool3 is: {deliver_by_bool3}')
                    elif wtime.time_difference(deliver_by_time, self.first_truck_delivery_times[1][-1]) > 0:
                        deliver_by_bool3 = True
                        print(f'[496] - deliver_by_bool3 is: {deliver_by_bool3}')
                    else:
                        deliver_by_bool3 = False
                        print(f'[499] - deliver_by_bool3 is: {deliver_by_bool3}')
                else:
                    print(f'deliver_by_time is: {deliver_by_time}')
                    print(f'self.third_truck_delivery_times[1][-1] is: {self.third_truck_delivery_times[1][-1]}')
                    if wtime.time_difference(deliver_by_time, self.third_truck_delivery_times[1][-1]) > 0:
                        deliver_by_bool3 = True
                        print(f'[505] - deliver_by_bool3 is: {deliver_by_bool3}')
                    # else:
                    #     if len(self.third_truck) > 0:
                    #         if wtime.time_difference(deliver_by_time, self.third_truck_delivery_times[1][0]) > 0:
                    #
                    else:
                        deliver_by_bool3 = False
                        print(f'[508] - deliver_by_bool3 is: {deliver_by_bool3}')

            # else:
            #     deliver_by_bool3 = True

            # Check if the package is delayed and can't be leaded until a specified time. If the specific package is
            # delayed, then it will be checked that the package doesn't get loaded on a truck that leaves before the
            # delayed package arrives. If the package can be loaded on the specified truck, then delayed_bool will be
            # True, if not, then it will be False.

            # Truck 1
            delayed_time1 = distance_list.get('Delayed ETA')
            if delayed_time1 is not None:
                if wtime.time_difference(FIRST_TRUCK_DEPARTURE_TIME, delayed_time1) >= 0:
                    delayed_bool1 = True
                else:
                    delayed_bool1 = False
            else:
                delayed_bool1 = True

            # Truck 2
            delayed_time2 = distance_list.get('Delayed ETA')
            if delayed_time2 is not None:
                # print(f"wtime.time_difference(self.second_truck_departure_time, delayed_time2) is: {wtime.time_difference(self.second_truck_departure_time, delayed_time2)}")
                if wtime.time_difference(self.second_truck_departure_time, delayed_time2) >= 0:
                    delayed_bool2 = True
                else:
                    delayed_bool2 = False
            else:
                delayed_bool2 = True

            # Truck 3
            delayed_time3 = distance_list.get('Delayed ETA')
            if delayed_time3 is not None:
                if len(self.first_truck) == 0:
                    delayed_bool3 = False
                    # continue
                elif wtime.time_difference(self.first_truck_delivery_times[1][-1], delayed_time3) >= 0:
                    delayed_bool3 = True
                else:
                    delayed_bool3 = False
            else:
                delayed_bool3 = True

            print(f'\nTruck 1 (Package {package_id}):')
            print(f'has_room_bool1 is: {has_room_bool1}')
            # print(f'load_on_truck1_bool is: {load_on_truck1_bool}')
            print(f'not truck 2 or not truck 3 is: {not load_on_truck2_bool or not load_on_truck3_bool}')
            print(f'deliver_by_bool1 is: {deliver_by_bool1}')
            print(f'delayed_bool1 is: {delayed_bool1}')

            print(f'\nTruck 2 (Package {package_id}):')
            print(f'has_room_bool2 is: {has_room_bool2}')
            # print(f'load_on_truck2_bool is: {load_on_truck2_bool}')
            print(f'not truck 1 or not truck 3 is: {not load_on_truck1_bool or not load_on_truck3_bool}')
            print(f'deliver_by_bool2 is: {deliver_by_bool2}')
            print(f'delayed_bool2 is: {delayed_bool2}')

            print(f'\nTruck 3 (Package {package_id}):')
            print(f'has_room_bool3 is: {has_room_bool3}')
            # print(f'load_on_truck3_bool is: {load_on_truck3_bool}')
            print(f'not truck 1 or not truck 2 is: {not load_on_truck1_bool or not load_on_truck2_bool}')
            print(f'deliver_by_bool3 is: {deliver_by_bool3}')
            print(f'delayed_bool3 is: {delayed_bool3}')

            # # For loop to get all the packages that are all going to the same address. For this dta set, worse case
            # # is 3 iterations, best case is 1 iteration.
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]

            #
            #             delayed_bool1 = False
            #
            #             #~~~~~~~~~~ Not in truck 2 or 3 ~~~~~~~~~
            #             print(f"Truck #: {distance_list.get('Truck')}")
            #             truck_num = distance_list.get('Truck')
            #             load_on_truck1_bool = True
            #             if truck_num is not None:
            #                 if truck_num == 2 or truck_num == 3:
            #                     load_on_truck1_bool = False
            #
            #             #~~~~~~~~~~ Deliver by ~~~~~~~~~~
            #             deliver_by_time = distance_list.get('Deliver By')
            #             deliver_by_bool1 = False
            #             if deliver_by_time is not None:
            #                 if deliver_by_time == 'EOD':
            #                     deliver_by_bool1 = False
            #                 else:
            #                     if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
            #                         deliver_by_bool1 = True
            #             else:
            #                 deliver_by_bool1 = True
            #
            #             #~~~~~~~~~~ Delivered with other packages ~~~~~~~~~~
            #
            #             # need_to_pack = self.packages_to_be_delivered_together.difference(self.first_truck)
            #             #
            #             # print(f'need_to_pack is: {need_to_pack}')
            #             #
            #             # if len(need_to_pack) == 1:
            #             #     if MAX_PACKAGES_PER_TRUCK - len(self.first_truck) - len(distance_list.get(need_to_pack)) == 0:
            #             #         for last_package in need_to_pack:
            #             #             delivery_info_dict[ppd.get_hash().lookup_item(int(last_package))[1][1]]
            #             #             print(f'last_package is: {last_package}')
            #             #             self.first_truck.append(distance_list.get('Package ID').get(last_package))
            #             #             self.been_loaded.append(distance_list.get('Package ID').get(last_package))
            #             #             self.total_packages_loaded += 1
            #
            #             #~~~~~~~~~~ Delayed eta ~~~~~~~~~~
            #
            #             # try:
            #             #     delayed_time = self.high_priority_packages[distance_list.get('Package ID').get(package_num)].get('Delayed ETA')
            #             # except KeyError:
            #             #     # print('No Delayed ETA high priority data')
            #             #     delayed_bool1 = True
            #             # except AttributeError:
            #             #     print('Cannot be "None"')
            #             #
            #             # else:
            #             #     if delayed_time is not None:
            #             #
            #             #         # XXXXXXXXXX Use WGUPS_time class XXXXXXXXXX
            #             #         (delayed_hours, delayed_minutes, delayed_seconds) = delayed_time.split(':')
            #             #         (first_hours, first_minutes, first_seconds) = FIRST_TRUCK_DEPARTURE_TIME.split(':')
            #             #         if int(delayed_hours) > int(first_hours):
            #             #             # print('Delayed package cant make it on truck 1 (hours)')
            #             #             delayed_bool1 = False
            #             #         elif int(delayed_hours) == int(first_hours):
            #             #             if int(delayed_minutes) > int(first_minutes):
            #             #                 # print('Delayed package cant make it on truck 1 (minutes)')
            #             #                 delayed_bool1 = False
            #             #             elif int(delayed_minutes) == int(first_minutes):
            #             #                 if int(delayed_seconds) > int(first_seconds):
            #             #                     # print('Delayed package cant make it on truck 1 (seconds)')
            #             #                     delayed_bool1 = False
            #             #
            #             #     else:
            #             #         # print('Okay to be on truck 1 (Delayed)')
            #             #         delayed_bool1 = True
            #
            #             # print(f"Package ID: {distance_list.get('Package ID').get(package_num)}")
            #             # print(f'delayed_bool1 is: {delayed_bool1}')
            #             # print(f'deliver_by_bool1 is {deliver_by_bool1}')
            #             # print(f'load_on_truck1_bool is: {load_on_truck1_bool}')
            #
            #             if load_on_truck1_bool and deliver_by_bool1:  #and delayed_bool1:

            # if distance_list.get('Package ID').get(package_num) not in self.first_truck:  # [O(n)]
            # if package_id not in self.first_truck:
                print(f"distance_list is: {distance_list}")
            # Truck 1
            # For loop to get all the packages that are all going to the same address. For this dta set, worse case
            # is 3 iterations, best case is 1 iteration.
            # for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                # print(f'T1 - self.been_loaded is: {self.been_loaded}')
                # print(f"T1 - distance_list.get('Package ID').get(package_num) is: {distance_list.get('Package ID').get(package_num)}")
                if distance_list.get('Package ID').get(package_num) not in self.been_loaded:  # [O(n)] ##### Consider moving this to the top of the function #####
                    if has_room_bool1 and (not load_on_truck2_bool or not load_on_truck3_bool) and deliver_by_bool1 and delayed_bool1:
                        self.first_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                        self.total_dist_first_truck = self.calculate_truck_distance(self.first_truck, delivery_info_dict)  # [O(n)]
                        self.first_truck_delivery_times = self.calculate_delivery_time(self.total_dist_first_truck[1], FIRST_TRUCK_DEPARTURE_TIME)  # [O(n)]
                    else:
                        not_loaded.add(distance_list.get('Package ID').get(package_num))
                #
            # Load Second Truck
            # elif len(self.second_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
            #
            #     # For loop to get all the packages that are all going to the same address. For this program, worse case
            #     # is 3 iterations, best case is 1 iteration.
            #     for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
            #
            #         # if distance_list.get('Package ID').get(package_num) not in self.second_truck:  # [O(n)]
            #         if distance_list.get('Package ID').get(package_num) not in self.been_loaded:  # [O(n)]
            #
            #             # delayed_bool1 = False
            #             # deliver_by_bool1 = True
            #
            #             #~~~~~~~~~~ Not in truck 1 or 3 ~~~~~~~~~
            #             truck_num = distance_list.get('Truck')
            #             load_on_truck2_bool = True
            #             if truck_num is not None:
            #                 if truck_num == 1 or truck_num == 3:
            #                     load_on_truck2_bool = False
            #
            #             # ~~~~~~~~~~ Deliver by ~~~~~~~~~~
            #             deliver_by_time = distance_list.get('Deliver By')
            #             deliver_by_bool2 = False
            #             if deliver_by_time is not None:
            #                 if deliver_by_time == 'EOD':
            #                     deliver_by_bool2 = False
            #                 else:
            #                     if len(self.second_truck) == 0:
            #                         if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
            #                             deliver_by_bool2 = True
            #                     else:
            #                         if wtime.time_difference(deliver_by_time, self.second_truck_delivery_times[1][-1]) > 0:
            #                             deliver_by_bool2 = True
            #             else:
            #                 deliver_by_bool2 = True
            #
            #             if len(self.third_truck) + len(distance_list.get('Package ID')) < MAX_PACKAGES_PER_TRUCK and deliver_by_bool2:
            #                 print('Truck 3 is NOT full!!!!!')
            #                 if load_on_truck2_bool:# and deliver_by_bool2:
            #
            #                     self.second_truck.append(distance_list.get('Package ID').get(package_num))
            #                     self.been_loaded.append(distance_list.get('Package ID').get(package_num))
            #                     self.total_packages_loaded += 1
            #                     self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck, delivery_info_dict)  # [O(n)]
            #                     self.second_truck_delivery_times = self.calculate_delivery_time(
            #                         self.total_dist_second_truck[1], self.second_truck_departure_time)  # [O(n)]
            #
            #             if len(self.third_truck) + len(distance_list.get('Package ID')) >= MAX_PACKAGES_PER_TRUCK:# and deliver_by_bool2:
            #                 print('Truck 3 is FULL!!!!!')
            #                 if load_on_truck2_bool:# or deliver_by_bool2:
            #

            # if package_id not in self.second_truck:

            # Truck 2
            # For loop to get all the packages that are all going to the same address. For this dta set, worse case
            # is 3 iterations, best case is 1 iteration.
            # for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                # print(f'T2 - self.been_loaded is: {self.been_loaded}')
                # print(f"T2 - distance_list.get('Package ID').get(package_num) is: {distance_list.get('Package ID').get(package_num)}")
                if distance_list.get('Package ID').get(package_num) not in self.been_loaded:  # [O(n)] ##### Consider moving this to the top of the function #####
                    if has_room_bool2 and (not load_on_truck1_bool or not load_on_truck3_bool) and deliver_by_bool2 and delayed_bool2:
                        self.second_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                        self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck, delivery_info_dict)  # [O(n)]
                        self.second_truck_delivery_times = self.calculate_delivery_time(
                            self.total_dist_second_truck[1], self.second_truck_departure_time)  # [O(n)]
                    # elif distance_list.get('Package ID').get(package_num) in not_loaded.difference(set(self.been_loaded)) and distance_list.get('Deliver By') != 'EOD' and has_room_bool2 and (not load_on_truck1_bool or not load_on_truck3_bool) and not deliver_by_bool2 and delayed_bool2:
                    #     self.second_truck.insert(0, distance_list.get('Package ID').get(package_num))
                    #     self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                    #     self.total_packages_loaded += 1
                    #     self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck,
                    #                                                                  delivery_info_dict)  # [O(n)]
                    #     self.second_truck_delivery_times = self.calculate_delivery_time(
                    #         self.total_dist_second_truck[1], self.second_truck_departure_time)  # [O(n)]
                    else:
                        not_loaded.add(distance_list.get('Package ID').get(package_num))
            #
            #
            # Load Third Truck
            # elif len(self.third_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
            #
            #     # For loop to get all the packages that are all going to the same address. For this program, worse case
            #     # is 3 iterations, best case is 1 iteration.
            #     for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
            #
            #         # if distance_list.get('Package ID').get(package_num) not in self.third_truck:
            #         if distance_list.get('Package ID').get(package_num) not in self.been_loaded:
            #
            #             #~~~~~~~~~~ Not in truck 1 or 2 ~~~~~~~~~
            #             truck_num = distance_list.get('Truck')
            #             load_on_truck3_bool = True
            #             if truck_num is not None:
            #                 if truck_num == 1 or truck_num == 2:
            #                     load_on_truck3_bool = False
            #
            #             #~~~~~~~~~~ Deliver by ~~~~~~~~~~
            #             deliver_by_time = distance_list.get('Deliver By')
            #             deliver_by_bool3 = False
            #             if deliver_by_time is not None:
            #                 if deliver_by_time == 'EOD':
            #                     deliver_by_bool3 = False
            #                 else:
            #                     if wtime.time_difference(deliver_by_time, self.first_truck_delivery_times[1][-1]) > 0:
            #                         deliver_by_bool3 = True
            #             else:
            #                 deliver_by_bool3 = True
            #
            #             # deliver_by_time = distance_list.get('Deliver By')
            #             # deliver_by_bool3 = False
            #             # if deliver_by_time is not None:
            #             #     if deliver_by_time == 'EOD':
            #             #         deliver_by_bool3 = True
            #             #     else:
            #             #         print('deliver_by_time is None')
            #             #         if len(self.third_truck) == 0:
            #             #             if wtime.time_difference(deliver_by_time, self.first_truck_delivery_times[1][-1]) > 0:
            #             #                 deliver_by_bool3 = True
            #             #             else:
            #             #                 print('This package needs to be on an earlier truck.')
            #             #         else:
            #             #             if wtime.time_difference(deliver_by_time, self.third_truck_delivery_times[1][-1]) > 0:
            #             #                 print('~~~~~ I MADE IT HERE (if)!!!!!! ~~~~~')
            #             #                 deliver_by_bool3 = True
            #             #             else:
            #             #                 print('~~~~~ I MADE IT HERE (else)!!!!!! ~~~~~')
                #             #                 backtracking = -1
            #             #                 while wtime.time_difference(deliver_by_time, self.third_truck_delivery_times[1][backtracking]) < 0:
            #             #                     backtracking -= 1
            #             #                     print(f'backtracking is: {backtracking}')
            #             #                 else:
            #             #                     self.third_truck.insert(backtracking - 1, distance_list.get('Package ID').get(package_num))
            #             #                     # self.third_truck.insert(len(self.third_truck) + backtracking, distance_list.get('Package ID').get(package_num))
            #             #                     self.been_loaded.append(distance_list.get('Package ID').get(package_num))
            #             #                     self.total_packages_loaded += 1
            #             #                     deliver_by_bool3 = False
            #
            #             if load_on_truck3_bool or deliver_by_bool3: #and delayed_bool3:

            # Truck 3

            # if package_id not in self.third_truck:

            # For loop to get all the packages that are all going to the same address. For this dta set, worse case
            # is 3 iterations, best case is 1 iteration.
            # for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                # print(f'T3 - self.been_loaded is: {self.been_loaded}')
                # print(f"T3 - distance_list.get('Package ID').get(package_num) is: {distance_list.get('Package ID').get(package_num)}")
                if distance_list.get('Package ID').get(package_num) not in self.been_loaded:  # [O(n)] ##### Consider moving this to the top of the function #####
                    # if has_room_bool3 and (not load_on_truck1_bool or not load_on_truck2_bool) and not deliver_by_bool3 and delayed_bool3:
                    #     while
                    if has_room_bool3 and (not load_on_truck1_bool or not load_on_truck2_bool) and deliver_by_bool3 and delayed_bool3:
                        self.third_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                        self.total_dist_third_truck = self.calculate_truck_distance(self.third_truck, delivery_info_dict)  # [O(n)]
                        self.third_truck_delivery_times = self.calculate_delivery_time(
                            self.total_dist_third_truck[1], self.first_truck_delivery_times[1][-1])  # [O(n)]
                    # elif has_room_bool3 and (not load_on_truck1_bool or not load_on_truck2_bool) and not deliver_by_bool3 and delayed_bool3:
                    #     self.third_truck.insert(0, distance_list.get('Package ID').get(package_num))
                    #     self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                    #     self.total_packages_loaded += 1
                    #     self.total_dist_third_truck = self.calculate_truck_distance(self.third_truck, delivery_info_dict)  # [O(n)]
                    #     self.third_truck_delivery_times = self.calculate_delivery_time(
                    #         self.total_dist_third_truck[1], self.first_truck_delivery_times[1][-1])  # [O(n)]
                    else:
                        not_loaded.add(distance_list.get('Package ID').get(package_num))


            # print(f'not_loaded is: {not_loaded.difference(set(self.been_loaded))}')
            print(f'Truck 1: {self.first_truck}')
            print(f'Truck 2: {self.second_truck}')
            print(f'Truck 3: {self.third_truck}')
            # print(f'total packages loaded is: {self.total_packages_loaded}')
        # # print(f'self.total_packages_loaded is: {self.total_packages_loaded}')
        # # print(f'len(ppd.get_input_data()) is {len(ppd.get_input_data())}')
        #
        # # Check if all the packages have been loaded
        # ##### Consider changing this to not be recursive #####
            if self.total_packages_loaded == len(ppd.get_input_data()):

                # Calculate the distance that each truck traveled
                # self.total_dist_first_truck = self.calculate_truck_distance(self.first_truck, delivery_info_dict)  # [O(n)]
                # self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck, delivery_info_dict)  # [O(n)]
                # self.total_dist_third_truck = self.calculate_truck_distance(self.third_truck, delivery_info_dict)  # [O(n)]

                # Calculate the time that each truck spent traveling to each destination.
                # self.first_truck_delivery_times = self.calculate_delivery_time(
                #     self.total_dist_first_truck[1], FIRST_TRUCK_DEPARTURE_TIME)  # [O(n)]
                # self.second_truck_delivery_times = self.calculate_delivery_time(
                #     self.total_dist_second_truck[1], self.second_truck_departure_time)  # [O(n)]
                # self.third_truck_delivery_times = self.calculate_delivery_time(
                #     self.total_dist_third_truck[1], self.first_truck_delivery_times[1][-1])  # [O(n)]

                self.delivery_data.append([self.first_truck, self.first_truck_delivery_times[1]])
                self.delivery_data.append([self.second_truck, self.second_truck_delivery_times[1]])
                self.delivery_data.append([self.third_truck, self.third_truck_delivery_times[1]])

                self.print_verbose_output()

            else:
                dist_list_index = distance_list.get("Index")  # [O(n)]
                # print(f'dist_list_index(address index) is: {dist_list_index}')
                shortest_dist = self.find_shortest_distance(ppd.get_distance_data(), int(dist_list_index)) # [O(n)]
                if shortest_dist in self.addresses:

                # if shortest_dist == 0:
                    shortest_dist = self.addresses[1]
                print(f'self.addresses is: {self.addresses}')
                print(f'sorted self.addresses is: {self.addresses.sort()}')
                print(f'self.been_loaded is {self.been_loaded}')
                print(f'sorted self.been_loaded is {self.been_loaded.sort()}')
                print(f'shortest_dist (index of nearest address) is: {shortest_dist}')
                dist_name = ppd.get_distance_name_data()[shortest_dist][2]  # [O(1)]
                # print(f'dist_name (nearest address) is: {dist_name}')
                package_id = delivery_info_dict.get(dist_name)['Package ID'][1]
                print(f'XXXXX Package_id is: {package_id} XXXXX')
                if package_id in self.been_loaded:
                    print('ITS ALREADY LOADED!!!!!!!')
                    print(f'not_loaded is: {not_loaded}')
                    if len(not_loaded) > 0 and len(self.been_loaded) > 0:
                        skipped = list(not_loaded.difference(set(self.been_loaded)))
                        print(f'skipped is: {skipped}')
                        if len(skipped) > 0:
                            package_id = skipped[0]

        #     # print(f'package_id is: {package_id}')
        #     # print(f"delivery_info_dict.get(dist_name) is: {delivery_info_dict.get(dist_name)}")
        #     # print(f"delivery_info_dict.get(dist_name)['Package ID'][1] is: {delivery_info_dict.get(dist_name)['Package ID'][1]}")
        #     # print(f'delivery_info_dict is: {delivery_info_dict}')
        #     # if delivery_info_dict.get(dist_name) is None:
        #
        #     # Call the load_trucks() method recursively until all packages are loaded.
        #     self.load_trucks(delivery_info_dict.get(dist_name)['Package ID'][1], delivery_info_dict)  # [O(n^2)]
        #     # try:
        #     #     self.load_trucks(delivery_info_dict.get(dist_name)['Package ID'][1], delivery_info_dict)  # [O(n^2)]
        #     # except TypeError:
        #     #     self.load_trucks(self.first_truck[0], delivery_info_dict)  # [O(n^2)]

    @staticmethod
    def convert_time(input_time):

        (input_hour, input_minute, input_second) = input_time.split(':')

        # Convert the delivery time string to datetime format
        return datetime.time(
            hour=int(input_hour),
            minute=int(input_minute),
            second=int(input_second)
        )

    # Update package status - [O(1)]
    # status_value --> 1 for "At the Hub", 2 for "En Route", or 3 for "Delivered at <time of delivery>
    def update_package_delivery_status_and_print_output(self, truck_list, truck_num, delivery_time_list, lookup_time):
    # def update_package_delivery_status(key, status_value, **kwargs):

        # status = ['At the hub', 'En route', f'Delivered at {kwargs["time"]}']
        #
        # value_index = 6  # The package status index
        #
        # ppd.get_hash().update_item(key, value_index, status[status_value])

        delivered_count = 0
        first_truck_diff = 0
        second_truck_diff = 0
        third_truck_diff = 0
        truck_status_options = ['At the hub', 'Delivering packages', 'Returned to the hub']
        package_status_options = ['At the hub', 'En route', 'Delivered']

        value_index = 6  # The package status index

        # Convert delivery time from string to datetime time
        converted_delivery_time_list = list(map(self.convert_time, delivery_time_list))

        # If user entered look up time is prior to the truck leaving the hub
        if ((truck_num == 1 and self.convert_time(FIRST_TRUCK_DEPARTURE_TIME) > lookup_time) or
                (truck_num == 2 and self.convert_time(self.second_truck_departure_time) > lookup_time) or
                (truck_num == 3 and self.convert_time(self.first_truck_delivery_times[1][-1]) > lookup_time)):
            truck_status = truck_status_options[0]

        # If user entered time is past the time that the truck has returned to the hub
        elif converted_delivery_time_list[-1] < lookup_time:
            truck_status = truck_status_options[2]

        # If the user entered time is after the truck left the hub, but before it has returned
        else:
            truck_status = truck_status_options[1]

        print('\n\n')
        print('-' * 126)

        # If the truck is either currently delivering packages or already returned to the hub
        if truck_status == truck_status_options[1] or truck_status == truck_status_options[2]:

            # First truck
            if truck_num == 1:
                print('|', f'Truck {truck_num} left the the hub at {FIRST_TRUCK_DEPARTURE_TIME}'.center(122), '|')

            # Second truck
            if truck_num == 2:
                print('|', f'Truck {truck_num} left the the hub at {self.second_truck_departure_time}'.center(122), '|')

            # Third truck
            if truck_num == 3:
                print('|', f'Truck {truck_num} left the the hub at {self.first_truck_delivery_times[1][-1]}'.center(122), '|')

            # If truck is currently delivering packages
            if truck_status == truck_status_options[1]:
                print('|', f'Truck {truck_num} status: {truck_status}'.center(122), '|')

            # If truck is not currently delivering packages
            else:
                print('|', f'Truck {truck_num} status: {truck_status} at {converted_delivery_time_list[-1]}'.center(122), '|')

        # If truck has not left the hub to deliver packages
        else:
            print(f'|', f'Truck {truck_num} status: {truck_status}'.center(122), '|')

        print('-' * 126)

        print(
            '|', 'ID'.center(2),
            '|', 'Address'.center(38),
            '|', 'Deliver By'.center(11),
            '|', 'City'.center(18),
            '|', 'Zip Code'.center(8),
            '|', 'Weight'.center(6),
            '|', 'Status'.center(21), '|'
        )

        print('-' * 126)

        for package_index in range(len(truck_list) + 1):

            if package_index >= len(truck_list):
                continue

            if truck_list[package_index] < 10:
                package_id = f' {str(truck_list[package_index])}'
            else:
                package_id = str(truck_list[package_index])

            # Package has been delivered
            if converted_delivery_time_list[package_index] <= lookup_time:
                ppd.get_hash().update_item(package_id, value_index, f'{package_status_options[2]} at {converted_delivery_time_list[package_index]}')
                delivered_count += 1

            # Package is en route
            elif truck_status == truck_status_options[1]:# and converted_delivery_time_list[package_index] >= lookup_time:
                ppd.get_hash().update_item(package_id, value_index, package_status_options[1])

            # Package is still at the hub
            else:
                ppd.get_hash().update_item(package_id, value_index, package_status_options[0])

            package_id = ppd.get_hash().lookup_item(package_id)[1][0]

            # Padding the single digits with a leading space for prettier output
            if int(package_id) < 10:
                package_id = ' ' + package_id

            address = ppd.get_hash().lookup_item(package_id)[1][1]
            deliver_by = ppd.get_hash().lookup_item(package_id)[1][2]
            city = ppd.get_hash().lookup_item(package_id)[1][3]
            zip_code = ppd.get_hash().lookup_item(package_id)[1][4]
            weight = ppd.get_hash().lookup_item(package_id)[1][5]
            status = ppd.get_hash().lookup_item(package_id)[1][6]

            print(
                f'| {package_id}'.ljust(3),
                f'| {address}'.ljust(40),
                f'| {deliver_by}'.ljust(13),
                f'| {city}'.ljust(20),
                f'| {zip_code}'.ljust(10),
                f'| {weight}'.ljust(8),
                f'| {status}'.ljust(23), '|',
                f' {ppd.sync_csv_data(ppd.get_hash().lookup_item(package_id))[address]}'
            )

        print('-' * 126)

        # Calculate first truck delivery duration
        if truck_num == 1:
            first_truck_diff = (datetime.timedelta(
                hours=int(self.first_truck_delivery_times[1][delivered_count - 1].split(':')[0]),
                minutes=int(self.first_truck_delivery_times[1][delivered_count - 1].split(':')[1]),
                seconds=int(self.first_truck_delivery_times[1][delivered_count - 1].split(':')[2])) -
                    datetime.timedelta(
                hours=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[0]),
                minutes=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[1]),
                seconds=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[2])
            ))

        # Calculate second truck delivery duration
        if truck_num == 2:
            second_truck_diff = (datetime.timedelta(
                hours=int(self.second_truck_delivery_times[1][delivered_count - 1].split(':')[0]),
                minutes=int(self.second_truck_delivery_times[1][delivered_count - 1].split(':')[1]),
                seconds=int(self.second_truck_delivery_times[1][delivered_count - 1].split(':')[2])) -
                    datetime.timedelta(
                hours=int(self.second_truck_departure_time.split(':')[0]),
                minutes=int(self.second_truck_departure_time.split(':')[1]),
                seconds=int(self.second_truck_departure_time.split(':')[2])
            ))

        # Calculate third truck delivery duration
        if truck_num == 3:
            third_truck_diff = (datetime.timedelta(
                hours=int(self.third_truck_delivery_times[1][delivered_count - 1].split(':')[0]),
                minutes=int(self.third_truck_delivery_times[1][delivered_count - 1].split(':')[1]),
                seconds=int(self.third_truck_delivery_times[1][delivered_count - 1].split(':')[2])) -
                    datetime.timedelta(
                hours=int(self.first_truck_delivery_times[1][-1].split(':')[0]),
                minutes=int(self.first_truck_delivery_times[1][-1].split(':')[1]),
                seconds=int(self.first_truck_delivery_times[1][-1].split(':')[2])
            ))

        # Calculate first truck delivery duration
        first_total_truck_diff = (datetime.timedelta(
            hours=int(self.first_truck_delivery_times[1][-1].split(':')[0]),
            minutes=int(self.first_truck_delivery_times[1][-1].split(':')[1]),
            seconds=int(self.first_truck_delivery_times[1][-1].split(':')[2])) -
                            datetime.timedelta(
            hours=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[0]),
            minutes=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[1]),
            seconds=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[2])
        ))

        # Calculate second truck delivery duration
        second_total_truck_diff = (datetime.timedelta(
            hours=int(self.second_truck_delivery_times[1][-1].split(':')[0]),
            minutes=int(self.second_truck_delivery_times[1][-1].split(':')[1]),
            seconds=int(self.second_truck_delivery_times[1][-1].split(':')[2])) -
                            datetime.timedelta(
            hours=int(self.second_truck_departure_time.split(':')[0]),
            minutes=int(self.second_truck_departure_time.split(':')[1]),
            seconds=int(self.second_truck_departure_time.split(':')[2])
        ))

        # Calculate third truck delivery duration
        third_total_truck_diff = (datetime.timedelta(
            hours=int(self.third_truck_delivery_times[1][-1].split(':')[0]),
            minutes=int(self.third_truck_delivery_times[1][-1].split(':')[1]),
            seconds=int(self.third_truck_delivery_times[1][-1].split(':')[2])) -
                            datetime.timedelta(
            hours=int(self.first_truck_delivery_times[1][-1].split(':')[0]),
            minutes=int(self.first_truck_delivery_times[1][-1].split(':')[1]),
            seconds=int(self.first_truck_delivery_times[1][-1].split(':')[2])
        ))

        if truck_status == truck_status_options[2]:

            if truck_num == 1:
                print('|', f'Truck 1 Summary: {len(self.first_truck)} packages were delivered in {first_total_truck_diff} and traveled {self.total_dist_first_truck[0]} miles.'.center(122), '|')
            if truck_num == 2:
                print('|', f'Truck 2 Summary: {len(self.second_truck)} packages were delivered in {second_total_truck_diff} and traveled {self.total_dist_second_truck[0]} miles.'.center(122), '|')
            if truck_num == 3:
                print('|', f'Truck 3 Summary: {len(self.third_truck)} packages were delivered in {third_total_truck_diff} and traveled {self.total_dist_third_truck[0]} miles.'.center(122), '|')

        elif truck_status == truck_status_options[1]:
            if truck_num == 1:
                if delivered_count == len(self.first_truck):
                    print('|', f'Truck 1 has delivered all {delivered_count} packages in {first_truck_diff} and has traveled {round(sum(self.total_dist_first_truck[1][:delivered_count]), 2)} miles and is heading back to the hub.'.center(122), '|')
                else:
                    print('|', f'Truck 1 has delivered {delivered_count}/{len(self.first_truck)} packages in {first_truck_diff} and has traveled {round(sum(self.total_dist_first_truck[1][:delivered_count]), 2)} miles.'.center(122), '|')
            if truck_num == 2:
                if delivered_count == len(self.second_truck):
                    print('|', f'Truck 2 has delivered all {delivered_count} packages in {second_truck_diff} and has traveled {round(sum(self.total_dist_second_truck[1][:delivered_count]), 2)} miles and is heading back to the hub.'.center(122), '|')
                else:
                    print('|', f'Truck 2 has delivered {delivered_count}/{len(self.second_truck)} packages in {second_truck_diff} and has traveled {round(sum(self.total_dist_second_truck[1][:delivered_count]), 2)} miles.'.center(122), '|')
            if truck_num == 3:
                if delivered_count == len(self.third_truck):
                    print('|', f'Truck 3 has delivered all {delivered_count} packages in {third_truck_diff} and has traveled {round(sum(self.total_dist_third_truck[1][:delivered_count]), 2)} miles and is heading back to the hub.'.center(122), '|')
                else:
                    print('|', f'Truck 3 has delivered {delivered_count}/{len(self.third_truck)} packages in {third_truck_diff} and has traveled {round(sum(self.total_dist_third_truck[1][:delivered_count]), 2)} miles.'.center(122), '|')

        else:
            print('|', f'Truck {truck_num} has not left the hub yet.'.center(122), '|')

        print('-' * 126)

        # All packages have been delivered and all trucks have returned to the hub
        self.total_distance_traveled = round(
            self.total_dist_first_truck[0] +
            self.total_dist_second_truck[0] +
            self.total_dist_third_truck[0], 2
        )

        self.total_delivery_time = (
                first_total_truck_diff +
                second_total_truck_diff +
                third_total_truck_diff
        )

        # Print output if truck 3 is the last truck to complete deliveries
        if self.convert_time(self.second_truck_delivery_times[1][-1]) <= self.convert_time(self.third_truck_delivery_times[1][-1]):
            if truck_status == truck_status_options[2] and truck_num == 3:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

        # Print output if truck 2 is the last truck to complete deliveries
        if self.convert_time(self.second_truck_delivery_times[1][-1]) >= self.convert_time(self.third_truck_delivery_times[1][-1]):
            if truck_status == truck_status_options[2] and truck_num == 2:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')
