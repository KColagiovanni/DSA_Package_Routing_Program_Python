from parse_package_data import Packages
from hash_table import HashTable
from wgups_time import WgupsTime

TABLE_SIZE = 40

ppd = Packages()
ht = HashTable(TABLE_SIZE)
wtime = WgupsTime()

DELIVERY_TRUCK_AVG_SPEED_MPH = 18
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

        self.truck_list = []
        self.been_loaded = []
        self.addresses = [0]
        self.distance_traveled = []
        self.delivery_data = []
        self.total_distance_traveled = []
        self.total_delivery_time = []

        self.packages_to_be_delivered_together = set(())

        self.second_truck_departure_time = ''
        self.total_packages_loaded = 0
        self.high_priority_count = 0

    # Truck 1 - [O(n)]
    def load_package_onto_first_truck(self, package_id):
        if len(self.first_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)] This wont changed with a bigger data set
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.first_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1

    # Truck 2 - [O(n)]
    def load_package_onto_second_truck(self, package_id):
        if len(self.second_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)] This wont changed with a bigger data set
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.second_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1

    # Truck 3 - [O(n)]
    def load_package_onto_third_truck(self, package_id):
        if len(self.third_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)] This wont changed with a bigger data set
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.third_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1

    # Manually load each truck by analyzing the package data (sync_csv_data) dictionary info to determine which truck
    # each package needs to be on. - [O(n)]
    def manual_load(self, record_data):

        # Adding the packages that must be on the same truck to a list.
        for record in record_data:  # [O(n)]
            deliver_together = record_data[record].get('Deliver Together')
            if deliver_together is not None:
                self.packages_to_be_delivered_together = deliver_together

        # Loading the packages that must go on the same truck together,prior to loading the rest of the packages.
        for package in self.packages_to_be_delivered_together:  # [O(n)]

            package_data = record_data[ppd.get_hash().lookup_item(package)[1][1]]  # [O(1)]
            package_id_data = package_data.get('Package ID')
            truck_num = package_data.get('Truck')
            delayed_eta = package_data.get('Delayed ETA')
            deliver_by_time = package_data.get('Deliver By')

            if truck_num is not None:
                truck = True
            else:
                truck = False

            if delayed_eta is not None:
                delayed = True
            else:
                delayed = False

            # If no conditions are defined, load onto first truck.
            if not truck and not delayed:
                self.load_package_onto_first_truck(package_id_data)

            # Load onto first truck
            if truck == 1:
                self.load_package_onto_first_truck(package_id_data)

            # Load onto second truck
            if truck == 2:
                self.load_package_onto_second_truck(package_id_data)

            # Load onto third truck
            if truck == 3:
                self.load_package_onto_third_truck(package_id_data)

            if deliver_by_time != 'EOD':
                # Truck 1
                if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                    self.load_package_onto_first_truck(package_id_data)

                # Truck 2
                if self.second_truck_departure_time != '':
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        self.load_package_onto_second_truck(package_id_data)

            # Truck 3
            else:
                self.load_package_onto_third_truck(package_id_data)

        # Load packages onto trucks that they are required to be on.
        for record in record_data:  # [O(n)]

            truck = record_data[record].get('Truck')
            package_id_data = record_data[record].get('Package ID')

            if truck is not None:

                # Load onto first truck
                if truck == 1:
                    self.load_package_onto_first_truck(package_id_data)

                # Load onto second truck
                if truck == 2:

                    self.load_package_onto_second_truck(package_id_data)

                # Load onto third truck
                if truck == 3:
                    self.load_package_onto_third_truck(package_id_data)

        # Determine which truck each package needs to be loaded onto based on whether it's delayed or not.
        for record in record_data:  # [O(n)]

            delayed_package = record_data[record].get('Delayed ETA')
            package_id_data = record_data[record].get('Package ID')
            deliver_by_time = record_data[record].get('Deliver By')

            if delayed_package is not None:

                # Truck 2
                if self.second_truck_departure_time == '':
                    self.second_truck_departure_time = delayed_package

                if deliver_by_time == 'EOD' and len(package_id_data) < 2:
                    self.load_package_onto_third_truck(package_id_data)

                if wtime.time_difference(self.second_truck_departure_time, delayed_package) >= 0:
                    self.second_truck_departure_time = delayed_package
                    self.load_package_onto_second_truck(package_id_data)

        # Determine which truck each package needs to be on based on it's "deliver by" time.
        for record in record_data:  # [O(n)]
            deliver_by_time = record_data[record].get('Deliver By')
            package_id_data = record_data[record].get('Package ID')

            if deliver_by_time is not None:

                if deliver_by_time != 'EOD':

                    # Truck 1
                    if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                        self.load_package_onto_first_truck(package_id_data)

                    # Truck 2
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        self.load_package_onto_second_truck(package_id_data)

                # Truck 3
                else:
                    if len(self.third_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_third_truck(package_id_data)
                    elif len(self.second_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_second_truck(package_id_data)
                    else:
                        self.load_package_onto_first_truck(package_id_data)

        self.truck_list = [self.first_truck, self.second_truck, self.third_truck]

        return self.truck_list

    # Returns the index of the shortest distance - [O(n^2)]
    def find_shortest_distance(self, distances, trucks_list, record_data):

        # Find the package with the shortest distance from the hub.
        for truck in range(len(trucks_list)):

            minimum_distance = float('inf')
            min_dist_package_address = ''
            ordered_truck_list = []
            loaded_in_ordered_list = []
            min_dist_index = ''

            # Find the package that is closest to the hub and add it to the first position in the truck.
            for package in trucks_list[truck]:
                package_address = ppd.get_hash().lookup_item(package)[1][1]
                package_index = int(record_data[package_address].get('Index'))

                if float(distances[package_index][0]) < minimum_distance:
                    minimum_distance = float(distances[package_index][0])
                    first_package_index_on_truck = trucks_list[truck].index(package)
                    min_dist_package_address = package_address
                    min_dist_index = package_index
                    # print(f'minimum_distance is: {minimum_distance}')
                    # print(f'first_package_index_on_truck is: {first_package_index_on_truck}')

            for package_num in record_data[min_dist_package_address].get('Package ID'):
                package_id = record_data[min_dist_package_address].get('Package ID')[package_num]
                # if package_id not in loaded_in_ordered_list:
                ordered_truck_list.append(package_id)
                self.addresses.append(min_dist_index)
                # loaded_in_ordered_list.append(package_id)

            package_index_list = []

            # Append the indexes of each package (going to the same address) on the truck, starting at index 1 because
            # the first package (index 0) has already been loaded.
            for packages in range(len(trucks_list[truck])):
                package_row = int(record_data[ppd.get_hash().lookup_item(trucks_list[truck][packages])[1][1]].get('Index'))
                if package_row not in package_index_list:
                    package_index_list.append(package_row)

            for packages in range(len(trucks_list[truck])):
                package_row = int(record_data[ppd.get_hash().lookup_item(ordered_truck_list[-1])[1][1]].get('Index'))
                min_dist = float('inf')
                min_dist_index = ''
                min_dist_package_id = ''

                # Traversing the distance list horizontally
                for package_index in range(len(package_index_list)):
                    if package_row > package_index_list[package_index]:
                        if distances[package_row][package_index_list[package_index]] != '':
                            if float(distances[package_row][package_index_list[package_index]]) < min_dist:
                                if package_index_list[package_index] not in self.addresses:
                                    min_dist = float(distances[package_row][package_index_list[package_index]])
                                    min_dist_index = package_index_list[package_index]
                                    min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]
                                    min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

                    # Traversing the distance list vertically
                    elif package_row < package_index_list[package_index]:
                        if distances[package_index_list[package_index]][package_row] != '':
                            if float(distances[package_index_list[package_index]][package_row]) < min_dist:
                                if package_index_list[package_index] not in self.addresses:
                                    min_dist = float(distances[package_index_list[package_index]][package_row])
                                    min_dist_index = package_index_list[package_index]
                                    min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]
                                    min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

                # print(f'\nmin_dist is: {min_dist}')
                # print(f'min_dist_index is: {min_dist_index}')
                # print(f'min_dist_truck_index is: {min_dist_truck_index}')
                # print(f'min_dist_index_address is: {min_dist_index_address}')
                # print(f"min_dist_package_id is: {min_dist_package_id}")

                for package_num in min_dist_package_id:
                    ordered_truck_list.append(min_dist_package_id[package_num])
                self.addresses.append(min_dist_index)

            trucks_list[truck] = ordered_truck_list
            print(f'Truck {truck + 1}({len(trucks_list[truck])}): {trucks_list[truck]}')

        self.first_truck = trucks_list[0]
        self.second_truck = trucks_list[1]
        self.third_truck = trucks_list[2]

        # Last minute adjustment
        triple_check = 0
        while triple_check < 1:
            for package_index in range(len(self.second_truck)):
                package_data = record_data[ppd.get_hash().lookup_item(self.second_truck[package_index])[1][1]]
                if len(package_data.get('Package ID')) == 1 and package_data.get('Deliver By') == 'EOD':
                    # print(f"\npackage id {package_data.get('Package ID')[1]} will be moved")
                    # print(f'package_index is: {package_index}')
                    # print(f'second_truck BEFORE: {self.second_truck}')
                    self.second_truck.append(self.second_truck[package_index])
                    # print(f'second_truck MIDDLE: {self.second_truck}')
                    self.second_truck.pop(package_index)
                    # print(f'second_truck AFTER: {self.second_truck}')
            triple_check += 1

        self.total_dist_first_truck = self.calculate_truck_distance(self.first_truck, record_data)  # [O(n)]
        self.total_dist_second_truck = self.calculate_truck_distance(self.second_truck, record_data)  # [O(n)]
        self.total_dist_third_truck = self.calculate_truck_distance(self.third_truck, record_data)  # [O(n)]

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

        return trucks_list

    # Calculate the delivery distance between each package in the loaded truck - [O(n)]
    @staticmethod
    def calculate_truck_distance(package_list, delivery_info_dict):

        truck_distance_list = []

        hub_to_first_delivery = float(ppd.get_distance_data()[int(
            delivery_info_dict.get(ppd.get_input_data()[package_list[0] - 1][1])["Index"]
        )][0])  # [O(1)]

        last_delivery_to_hub = float(ppd.get_distance_data()[int(
                delivery_info_dict.get(ppd.get_input_data()[package_list[-1] - 1][1])["Index"]
        )][0])  # [O(1)]

        # Distance from the hub to the first address.
        truck_distance_list.append(hub_to_first_delivery)

        # Iterate over each package list
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

        # (hours, minutes, seconds) = departure_time.split(':')
        # converted_departure_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

        cumulative_delivery_duration_list = []
        delivery_time_list = []
        total_duration = 0.0
        # print(f'\ntotal_duration before for loop is: {total_duration}')

        for package_distance in package_distance_list:

            duration = round((package_distance / DELIVERY_TRUCK_AVG_SPEED_MPH), 2) * 3600
            # print(f'duration is: {duration}')

            # print(f'type(total_duration) before is {type(total_duration)}')
            # print(f'total_duration before is {total_duration}')
            if type(total_duration) is float:
                # print('in total_duration if')
                total_duration = wtime.convert_int_seconds_to_string_time(int(total_duration))
            # print(f'type(total_duration) after is {type(total_duration)}')
            # print(f'total_duration after is {total_duration}')

            # print(f'type(duration) before is: {type(duration)}')
            # print(f'duration before is: {duration}')
            if type(duration) is float:
                # print('in duration if')
                duration = wtime.convert_int_seconds_to_string_time(int(duration))
            # print(f'type(duration) after is {type(duration)}')
            # print(f'duration after is: {duration}')

            total_duration = wtime.add_time(total_duration, duration)
            # total_duration += duration
            # print(f'total_duration in for loop is: {total_duration}')

            # total_duration_seconds = total_duration * 3600
            # print(f'total_duration_seconds is: {total_duration_seconds}')

            # total_duration = wtime.convert_int_seconds_to_string_time(total_duration)
            # print(f'total_duration is: {total_duration}')

            # print(f'departure_time is: {departure_time}')
            cumulative_delivery_duration_list.append(wtime.add_time(departure_time, total_duration))
            # print(f'cumulative_delivery_duration_list is {cumulative_delivery_duration_list}')

            # cumulative_delivery_duration_list.append(
                # str(converted_departure_time + datetime.timedelta(hours=float(total_duration))))
            # delivery_time_list.append(str(datetime.timedelta(hours=float(duration))))

            # print(f'duration({duration}) is being appended to delivery_time_list')
            delivery_time_list.append(duration)

            # print(f'deliver_time_list is: {delivery_time_list}')

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

    # Update package status - [O(1)]
    # status_value --> 1 for "At the Hub", 2 for "En Route", or 3 for "Delivered at <time of delivery>
    def update_package_delivery_status_and_print_output_for_all_packages(
            self,
            truck_list,
            truck_num,
            delivery_time_list,
            lookup_time
    ):

        delivered_count = 0
        first_truck_diff = 0
        second_truck_diff = 0
        third_truck_diff = 0
        truck_status_options = ['At the hub', 'Delivering packages', 'Returned to the hub']
        package_status_options = ['At the hub', 'En route', 'Delivered']

        value_index = 6  # The package status index

        # If user entered look up time is prior to the truck leaving the hub
        if ((truck_num == 1 and wtime.time_difference(FIRST_TRUCK_DEPARTURE_TIME, lookup_time) > 0) or
                (truck_num == 2 and wtime.time_difference(self.second_truck_departure_time, lookup_time) > 0) or
                (truck_num == 3 and wtime.time_difference(self.first_truck_delivery_times[1][-1], lookup_time) > 0)):
            truck_status = truck_status_options[0]

        # If user entered time is past the time that the truck has returned to the hub
        elif wtime.time_difference(lookup_time, delivery_time_list[-1]) > 0:
            truck_status = truck_status_options[2]

        # If the user entered time is after the truck left the hub, but before it has returned
        else:
            truck_status = truck_status_options[1]

        # Print package information
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
                print('|', f'Truck {truck_num} status: {truck_status} at {delivery_time_list[-1]}'.center(122), '|')

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

            # Padding the single digits with a leading space for prettier output
            if truck_list[package_index] < 10:
                package_id = f' {str(truck_list[package_index])}'
            else:
                package_id = str(truck_list[package_index])

            # Package has been delivered
            if wtime.time_difference(lookup_time, delivery_time_list[package_index]) > 0:
                ppd.get_hash().update_item(package_id, value_index, f'{package_status_options[2]} at {delivery_time_list[package_index]}')
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
            first_truck_diff = wtime.time_difference(self.first_truck_delivery_times[1][delivered_count - 1], FIRST_TRUCK_DEPARTURE_TIME)
            first_truck_diff = wtime.convert_int_seconds_to_string_time(first_truck_diff)

        # Calculate second truck delivery duration
        if truck_num == 2:
            second_truck_diff = wtime.time_difference(self.second_truck_delivery_times[1][delivered_count - 1], self.second_truck_departure_time)
            second_truck_diff = wtime.convert_int_seconds_to_string_time((second_truck_diff))

        # Calculate third truck delivery duration
        if truck_num == 3:
            third_truck_diff = wtime.time_difference(self.third_truck_delivery_times[1][delivered_count - 1], self.first_truck_delivery_times[1][-1])
            third_truck_diff = wtime.convert_int_seconds_to_string_time(third_truck_diff)

        # Calculate first truck delivery duration
        first_total_truck_diff = wtime.time_difference(self.first_truck_delivery_times[1][-1], FIRST_TRUCK_DEPARTURE_TIME)
        first_total_truck_diff = wtime.convert_int_seconds_to_string_time(first_total_truck_diff)

        # Calculate second truck delivery duration
        second_total_truck_diff = wtime.time_difference(self.second_truck_delivery_times[1][-1], self.second_truck_departure_time)
        second_total_truck_diff = wtime.convert_int_seconds_to_string_time(second_total_truck_diff)

        # Calculate third truck delivery duration
        third_total_truck_diff = wtime.time_difference(self.third_truck_delivery_times[1][-1], self.first_truck_delivery_times[1][-1])
        third_total_truck_diff = wtime.convert_int_seconds_to_string_time(third_total_truck_diff)

        if truck_status == truck_status_options[2]:

            if truck_num == 1:
                print(f'first_truck is: {self.first_truck}')
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
                wtime.convert_string_time_to_int_seconds(first_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(second_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(third_total_truck_diff)
        )

        self.total_delivery_time = wtime.convert_int_seconds_to_string_time(self.total_delivery_time)

        # Print output if truck 3 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[1][-1], self.second_truck_delivery_times[1][-1]) >= 0:
            if truck_status == truck_status_options[2] and truck_num == 3:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

        # Print output if truck 2 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[1][-1], self.second_truck_delivery_times[1][-1]) <= 0:
            if truck_status == truck_status_options[2] and truck_num == 2:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

    def update_package_delivery_status_and_print_output_for_single_package(self, truck_list, truck_num, delivery_time_list, lookup_time, package_id):
        delivered_count = 0
        first_truck_diff = 0
        second_truck_diff = 0
        third_truck_diff = 0
        truck_status_options = ['At the hub', 'Delivering packages', 'Returned to the hub']
        package_status_options = ['At the hub', 'En route', 'Delivered']

        value_index = 6  # The package status index

        # If user entered look up time is prior to the truck leaving the hub
        if ((truck_num == 1 and wtime.time_difference(FIRST_TRUCK_DEPARTURE_TIME, lookup_time) > 0) or
                (truck_num == 2 and wtime.time_difference(self.second_truck_departure_time, lookup_time) > 0) or
                (truck_num == 3 and wtime.time_difference(self.first_truck_delivery_times[1][-1], lookup_time) > 0)):
            truck_status = truck_status_options[0]

        # If user entered time is past the time that the truck has returned to the hub
        elif wtime.time_difference(lookup_time, delivery_time_list[-1]) > 0:
            truck_status = truck_status_options[2]

        # If the user entered time is after the truck left the hub, but before it has returned
        else:
            truck_status = truck_status_options[1]

        # Print package information
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
                print('|', f'Truck {truck_num} status: {truck_status} at {delivery_time_list[-1]}'.center(122), '|')

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

            # Padding the single digits with a leading space for prettier output
            if truck_list[package_index] < 10:
                package_id_loop = f' {str(truck_list[package_index])}'
            else:
                package_id_loop = str(truck_list[package_index])

        # Package has been delivered
        if wtime.time_difference(lookup_time, delivery_time_list[package_index]) > 0:
            ppd.get_hash().update_item(package_id, value_index, f'{package_status_options[2]} at {delivery_time_list[package_index]}')
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
            first_truck_diff = wtime.time_difference(self.first_truck_delivery_times[1][delivered_count - 1], FIRST_TRUCK_DEPARTURE_TIME)
            first_truck_diff = wtime.convert_int_seconds_to_string_time(first_truck_diff)

        # Calculate second truck delivery duration
        if truck_num == 2:
            second_truck_diff = wtime.time_difference(self.second_truck_delivery_times[1][delivered_count - 1], self.second_truck_departure_time)
            second_truck_diff = wtime.convert_int_seconds_to_string_time((second_truck_diff))

        # Calculate third truck delivery duration
        if truck_num == 3:
            third_truck_diff = wtime.time_difference(self.third_truck_delivery_times[1][delivered_count - 1], self.first_truck_delivery_times[1][-1])
            third_truck_diff = wtime.convert_int_seconds_to_string_time(third_truck_diff)

        # Calculate first truck delivery duration
        first_total_truck_diff = wtime.time_difference(self.first_truck_delivery_times[1][-1], FIRST_TRUCK_DEPARTURE_TIME)
        first_total_truck_diff = wtime.convert_int_seconds_to_string_time(first_total_truck_diff)

        # Calculate second truck delivery duration
        second_total_truck_diff = wtime.time_difference(self.second_truck_delivery_times[1][-1], self.second_truck_departure_time)
        second_total_truck_diff = wtime.convert_int_seconds_to_string_time(second_total_truck_diff)

        # Calculate third truck delivery duration
        third_total_truck_diff = wtime.time_difference(self.third_truck_delivery_times[1][-1], self.first_truck_delivery_times[1][-1])
        third_total_truck_diff = wtime.convert_int_seconds_to_string_time(third_total_truck_diff)

        if truck_status == truck_status_options[2]:

            if truck_num == 1:
                print(f'first_truck is: {self.first_truck}')
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
                wtime.convert_string_time_to_int_seconds(first_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(second_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(third_total_truck_diff)
        )

        self.total_delivery_time = wtime.convert_int_seconds_to_string_time(self.total_delivery_time)

        # Print output if truck 3 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[1][-1], self.second_truck_delivery_times[1][-1]) >= 0:
            if truck_status == truck_status_options[2] and truck_num == 3:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

        # Print output if truck 2 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[1][-1], self.second_truck_delivery_times[1][-1]) <= 0:
            if truck_status == truck_status_options[2] and truck_num == 2:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')
