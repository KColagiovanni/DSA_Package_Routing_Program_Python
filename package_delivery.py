from parse_package_data import Packages
from hash_table import HashTable
import datetime
from datetime import time

ppd = Packages()
ht = HashTable()

DELIVERY_TRUCK_SPEED_MPH = 18
MAX_PACKAGES_PER_TRUCK = 16
FIRST_TRUCK_DEPARTURE_TIME = '8:00:00'


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

        self.delivery_status = {}

        self.second_truck_departure_time = ''
        self.total_packages_loaded = 0
        self.high_priority_count = 0

    # Analyze the special notes and deliver by times and add packages to trucks as needed - [O(1)]
    def analyze_package_data(self, key):

        package_data = ppd.get_hash().lookup_item(key)  # O(1)
        packages_to_be_delivered_together = set(())

        # ~~~~~~~~~~ Try using REGEX here ~~~~~~~~~~ #
        if 'Must be delivered with' in package_data[1][7]:
            package1 = int(package_data[1][7][-7:-5])
            packages_to_be_delivered_together.add(package1)
            package2 = int(package_data[1][7][-2:])
            packages_to_be_delivered_together.add(package2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # Determine priority and load delayed packages on later trucks
        if 'Delayed on flight' in package_data[1][7]:
            package_eta = package_data[1][7][-7:-3]
            if package_data[1][2] != 'EOD':
                # print(f'DELAYED | HIGH PRIORITY: {package_data[0]}'
                # f'- ETA: {package_eta} (Deliver by: {package_data[1][2]})')
                self.second_truck.insert(self.high_priority_count, int(package_data[0]))
                self.high_priority_count += 0
                self.been_loaded.append(int(package_data[0]))
                self.total_packages_loaded += 1
                self.second_truck_departure_time = package_eta + ':00'
            else:
                # print(f'DELAYED | {package_data[0]} - ETA: {package_eta} (Deliver by: {package_data[1][2]})')
                self.third_truck.append(int(package_data[0]))
                self.been_loaded.append(int(package_data[0]))
                self.total_packages_loaded += 1

        # Loading packages into the specific trucks that special instructions request.
        if 'Can only be on truck' in package_data[1][7]:

            # For truck 1
            if package_data[1][7][-1] == '1':
                if int(package_data[0]) not in self.first_truck:
                    self.first_truck.append(int(package_data[0]))
                    self.been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1

            # For truck 2
            elif package_data[1][7][-1] == '2':
                if int(package_data[0]) not in self.second_truck:
                    self.second_truck.append(int(package_data[0]))
                    self.been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1

            # For truck 3
            elif package_data[1][7][-1] == '3':
                if int(package_data[0]) not in self.third_truck:
                    self.third_truck.append(int(package_data[0]))
                    self.been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1

    # Returns the index of the shortest distance - [O(n)]
    def find_shortest_distance(self, distances, search_row_index):

        search_data = {
            'min_horizontal_index': 0,
            'min_vertical_index': 0,
            'traversal_direction': 'horizontal',
            'min_dist': float(distances[search_row_index][1]),
            'min_dist_location': 'horizontal'
        }

        for row in range(1, len(distances[search_row_index])):

            if distances[search_row_index][row] == '0.0':
                search_data['traversal_direction'] = 'vertical'

            if row in self.addresses:
                continue

            if search_data['traversal_direction'] == 'horizontal':
                if distances[search_row_index][row] != '':
                    if float(distances[search_row_index][row]) < search_data['min_dist']:
                        if float(distances[search_row_index][row]) != 0:
                            search_data['min_dist'] = float(distances[search_row_index][row])
                            search_data['min_dist_location'] = 'horizontal'
                            search_data['min_horizontal_index'] = row

            if search_data['traversal_direction'] == 'vertical':
                if distances[row][search_row_index] != '':
                    if float(distances[row][search_row_index]) < search_data['min_dist']:
                        if float(distances[row][search_row_index]) != 0:
                            search_data['min_dist'] = float(distances[row][search_row_index])
                            search_data['min_dist_location'] = 'vertical'
                            search_data['min_vertical_index'] = row

        self.distance_traveled.append(float(search_data["min_dist"]))

        if search_row_index not in self.addresses:
            self.addresses.append(search_row_index)

        if search_data["min_horizontal_index"] == 0 and search_data["min_vertical_index"] == 0:
            for index in range(1, len(distances[search_row_index])):
                if index not in self.addresses:
                    search_data['min_horizontal_index'] = index
                    search_data['min_vertical_index'] = index

        if search_data['min_dist_location'] == 'horizontal':
            return search_data['min_horizontal_index']
        if search_data['min_dist_location'] == 'vertical':
            return search_data['min_vertical_index']

    # Check if a truck can be loaded more efficiently if it was initially loaded with
    # required packages prior to being loaded by the shortest distance method
    def maximize_efficiency(self, index):
        pass

    # Calculate the delivery distance between each package in the loaded truck - [O(n)]
    @staticmethod
    def calculate_truck_distance(package_list, delivery_info_dict):

        truck_distance_list = []

        hub_to_first_delivery = float(ppd.get_distance_data()[int(
            delivery_info_dict.get(ppd.get_input_data()[package_list[0]][1])["Index"]
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

    # Loads packages onto the trucks, using recursion - [O(n^2)]
    def load_trucks(self, package_id, delivery_info_dict):

        package_id_data = ppd.get_input_data()[int(package_id) - 1]
        distance_list = delivery_info_dict[ppd.get_hash().lookup_item(int(package_id_data[0]))[1][1]]  # [O(1)]

        # Load First Truck
        if len(self.first_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:

            # For loop to get all the packages that are all going to the same address. For this program, worse case
            # is 3 iterations, best case is 1 iteration.
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.first_truck:
                    if distance_list.get('Package ID').get(package_num) not in self.been_loaded:
                        self.first_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Second Truck
        elif len(self.second_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:

            # For loop to get all the packages that are all going to the same address. For this program, worse case
            # is 3 iterations, best case is 1 iteration.
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.second_truck:
                    if distance_list.get('Package ID').get(package_num) not in self.been_loaded:
                        self.second_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Third Truck
        elif len(self.third_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:

            # For loop to get all the packages that are all going to the same address. For this program, worse case
            # is 3 iterations, best case is 1 iteration.
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):  # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.third_truck:
                    if distance_list.get('Package ID').get(package_num) not in self.been_loaded:
                        self.third_truck.append(distance_list.get('Package ID').get(package_num))
                        self.been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        else:
            return

        # Check if all the packages have been loaded
        ##### Consider changing this to not be recursive #####
        if self.total_packages_loaded == len(ppd.get_input_data()):

            # Calculate the distance that each truck traveled
            self.total_dist_first_truck = self.calculate_truck_distance(self.first_truck, delivery_info_dict)  # [O(n)]
            self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck, delivery_info_dict)  # [O(n)]
            self.total_dist_third_truck = self.calculate_truck_distance(self.third_truck, delivery_info_dict)  # [O(n)]

            # Calculate the time that each truck spent traveling to each destination.
            self.first_truck_delivery_times = self.calculate_delivery_time(
                self.total_dist_first_truck[1], FIRST_TRUCK_DEPARTURE_TIME)  # [O(n)]
            self.second_truck_delivery_times = self.calculate_delivery_time(
                self.total_dist_second_truck[1], self.second_truck_departure_time)  # [O(n)]
            self.third_truck_delivery_times = self.calculate_delivery_time(
                self.total_dist_third_truck[1], self.first_truck_delivery_times[1][-1])  # [O(n)]

            self.delivery_data.append([self.first_truck, self.first_truck_delivery_times[1]])
            self.delivery_data.append([self.second_truck, self.second_truck_delivery_times[1]])
            self.delivery_data.append([self.third_truck, self.third_truck_delivery_times[1]])

            self.print_verbose_output()

        else:
            dist_list_index = distance_list.get("Index")  # [O(n)]
            shortest_dist = self.find_shortest_distance(ppd.get_distance_data(), int(dist_list_index))  # [O(n)]
            dist_name = ppd.get_distance_name_data()[shortest_dist][2]  # [O(1)]
            self.load_trucks(delivery_info_dict.get(dist_name)["Package ID"][1], delivery_info_dict)  # [O(n^2)]

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
    def update_package_delivery_status(self, truck_list, truck_num, delivery_time_list, lookup_time):
    # def update_package_delivery_status(key, status_value, **kwargs):

        # status = ['At the hub', 'En route', f'Delivered at {kwargs["time"]}']
        #
        # value_index = 6  # The package status index
        #
        # ppd.get_hash().update_item(key, value_index, status[status_value])

        truck_status = ''
        package_status = ''
        truck_status_options = ['Has not left the hub', 'Delivering packages', 'Returned to the hub']
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

        # If the truck is either currently delivering packages or already returned to the hub
        if truck_status == truck_status_options[1] or truck_status == truck_status_options[2]:

            # First truck
            if truck_num == 1:
                print(f'\n\nTruck {truck_num} left the the hub at {FIRST_TRUCK_DEPARTURE_TIME}')

            # Second truck
            if truck_num == 2:
                print(f'\n\nTruck {truck_num} left the the hub at {self.second_truck_departure_time}')

            # Third truck
            if truck_num == 3:
                print(f'\n\nTruck {truck_num} left the the hub at {self.first_truck_delivery_times[1][-1]}')

            # If truck is currently delivering packages
            if truck_status == truck_status_options[1]:
                print(f'Truck {truck_num} status is: {truck_status}')

            # If truck is not currently delivering packages
            else:
                print(f'Truck {truck_num} status is: {truck_status} at {converted_delivery_time_list[-1]}')

        # If truck has not left the hub to deliver packages
        else:
            print(f'\n\nTruck {truck_num} status is: {truck_status}')

        print('-' * 40)

        for package_index in range(len(truck_list) + 1):

            if package_index >= len(truck_list):
                # print()
                continue

            if truck_list[package_index] < 10:
                package_id = f' {str(truck_list[package_index])}'
            else:
                package_id = str(truck_list[package_index])

            # Package has been delivered
            if converted_delivery_time_list[package_index] <= lookup_time:
                print(f'Package {package_id} Status: {package_status_options[2]} at {converted_delivery_time_list[package_index]}')

            # Package is en route
            elif truck_status == truck_status_options[1]:# and converted_delivery_time_list[package_index] >= lookup_time:
                print(f'Package {package_id} Status: {package_status_options[1]}')

            # Package is still at the hub
            else:
                print(f'Package {package_id} Status: {package_status_options[0]}')


        if truck_status == truck_status_options[2]:
            print('-' * 40)

            # Calculate first truck delivery duration
            first_truck_diff = (datetime.timedelta(
                hours=int(self.first_truck_delivery_times[1][-1].split(':')[0]),
                minutes=int(self.first_truck_delivery_times[1][-1].split(':')[1]),
                seconds=int(self.first_truck_delivery_times[1][-1].split(':')[2])) -
                                datetime.timedelta(
                hours=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[0]),
                minutes=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[1]),
                seconds=int(FIRST_TRUCK_DEPARTURE_TIME.split(':')[2])
            ))

            # Calculate second truck delivery duration
            second_truck_diff = (datetime.timedelta(
                hours=int(self.second_truck_delivery_times[1][-1].split(':')[0]),
                minutes=int(self.second_truck_delivery_times[1][-1].split(':')[1]),
                seconds=int(self.second_truck_delivery_times[1][-1].split(':')[2])) -
                                datetime.timedelta(
                hours=int(self.second_truck_departure_time.split(':')[0]),
                minutes=int(self.second_truck_departure_time.split(':')[1]),
                seconds=int(self.second_truck_departure_time.split(':')[2])
            ))

            # Calculate third truck delivery duration
            third_truck_diff = (datetime.timedelta(
                hours=int(self.third_truck_delivery_times[1][-1].split(':')[0]),
                minutes=int(self.third_truck_delivery_times[1][-1].split(':')[1]),
                seconds=int(self.third_truck_delivery_times[1][-1].split(':')[2])) -
                                datetime.timedelta(
                hours=int(self.first_truck_delivery_times[1][-1].split(':')[0]),
                minutes=int(self.first_truck_delivery_times[1][-1].split(':')[1]),
                seconds=int(self.first_truck_delivery_times[1][-1].split(':')[2])
            ))

            if truck_num == 1:
                print(f'Truck 1 delivered {len(self.first_truck)} packages in {first_truck_diff} and traveled {self.total_dist_first_truck[0]} miles.')
            if truck_num == 2:
                print(f'Truck 2 delivered {len(self.second_truck)} packages in {second_truck_diff} and traveled {self.total_dist_second_truck[0]} miles.')
            if truck_num == 3:
                print(f'Truck 3 delivered {len(self.third_truck)} packages in {third_truck_diff} and traveled {self.total_dist_third_truck[0]} miles.')

            # All packages have been delivered and all trucks have returned to the hub
            self.total_distance_traveled = round(
                self.total_dist_first_truck[0] +
                self.total_dist_second_truck[0] +
                self.total_dist_third_truck[0], 2
            )

            self.total_delivery_time = (
                    first_truck_diff +
                    second_truck_diff +
                    third_truck_diff
            )

        if self.convert_time(self.second_truck_delivery_times[1][-1]) > self.convert_time(self.third_truck_delivery_times[1][-1]):
            if self.convert_time(self.second_truck_delivery_times[1][-1]) < lookup_time and truck_num == 3:
                print(f'\nTotal Distance Traveled: {self.total_distance_traveled} miles')
                print(f'Total delivery time: {self.total_delivery_time} (HH:MM:SS)')
            # else:
