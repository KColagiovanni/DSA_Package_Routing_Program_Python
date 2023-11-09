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

            # Checking if the truck exists
            if truck_num is not None:
                truck = True
            else:
                truck = False

            # Checking if the package is delayed
            if delayed_eta is not None:
                delayed = True
            else:
                delayed = False

            # If no conditions are defined, load onto first truck.
            if not truck and not delayed:
                self.load_package_onto_first_truck(package_id_data)

            # Must be on first truck
            if truck == 1:
                self.load_package_onto_first_truck(package_id_data)

            # Must be on second truck
            if truck == 2:
                self.load_package_onto_second_truck(package_id_data)

            # Must be on third truck
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

                # Truck 3
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

                    # If deliver by time is after the departure time of the first truck
                    if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                        self.load_package_onto_first_truck(package_id_data)

                    # If deliver by time is after the departure time of the second truck
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        self.load_package_onto_second_truck(package_id_data)

                # Truck 3
                else:
                    # If deliver by time is "EOD" and truck 3 is not full
                    if len(self.third_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_third_truck(package_id_data)
                    # If deliver by time is "EOD" and truck 3 is full, but truck 2 is not full
                    elif len(self.second_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_second_truck(package_id_data)
                    # If deliver by time is "EOD" and trucks 2 and 3 are full, but truck 1 is not full
                    else:
                        self.load_package_onto_first_truck(package_id_data)

        self.truck_list = [self.first_truck, self.second_truck, self.third_truck]

        return self.truck_list

    # Returns the index of the shortest distance - [O(n^2)]
    def find_shortest_distance(self, distances, package_list, truck_num, record_data):

        print(f'\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Truck {truck_num + 1} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        delivery_times_list = []
        min_dist = float('inf')
        min_dist_index = ''
        min_dist_package_address = ''
        ordered_truck_list = []
        package_index_list = []
        total_truck_dist = []

        # Find the package that is closest to the hub.
        for package in package_list:
            package_address = ppd.get_hash().lookup_item(package)[1][1]
            package_index_in_record_data = int(record_data[package_address].get('Index'))
            if float(distances[package_index_in_record_data][0]) < min_dist:
                min_dist = float(distances[package_index_in_record_data][0])
                min_dist_package_address = package_address
                min_dist_index = package_index_in_record_data
        self.addresses.append(min_dist_index)

        # Add the first package to the first position in the truck and calculate the delivery time.
        for package_num in record_data[min_dist_package_address].get('Package ID'):
            package_id = record_data[min_dist_package_address].get('Package ID')[package_num]
            ordered_truck_list.append(package_id)

            # If there are multiple packages going to the same address, package 1 will be the first.
            if package_num == 1:
                if truck_num == 0:
                    delivery_time_seconds = self.calculate_delivery_time(min_dist)
                    delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(wtime.add_time(delivery_time, FIRST_TRUCK_DEPARTURE_TIME)))  # [O(n)]
                elif truck_num == 1:
                    delivery_time_seconds = self.calculate_delivery_time(min_dist)
                    delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(wtime.add_time(delivery_time, self.second_truck_departure_time)))  # [O(n)]
                elif truck_num == 2 and len(self.first_truck_delivery_times) > 0:
                    delivery_time_seconds = self.calculate_delivery_time(min_dist)
                    delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(wtime.add_time(delivery_time, self.first_truck_delivery_times[-1])))  # [O(n)]
                else:
                    raise ValueError("This method wasn't designed to handle more than 3 trucks")

                total_truck_dist.append(min_dist)

            # Add subsequent packages that are going to the same address
            else:
                delivery_time_seconds = self.calculate_delivery_time(0.0)
                delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                # print(f"appending {record_data[min_dist_package_address].get('Package ID')[package_num]}(first package) to {ordered_truck_list}")
                delivery_times_list.append(wtime.convert_int_seconds_to_string_time(wtime.add_time('00:00:00', delivery_times_list[-1])))  # [O(n)]
                # print(f"appending 0.0(first package) to {total_truck_dist}")
                total_truck_dist.append(0.0)

        # Append the indexes of each package (going to the same address) to the truck, starting at index 1 because
        # the first package (index 0) has already been loaded.
        for packages in range(len(package_list)):
            package_row_index = int(record_data[ppd.get_hash().lookup_item(package_list[packages])[1][1]].get('Index'))
            if package_row_index not in package_index_list:
                package_index_list.append(package_row_index)

        # Iterate over each package on the truck that has been manually loaded.
        # for packages in range(len(package_list)):
        packages = 1
        while packages < len(package_list):

            package_row_index = int(record_data[ppd.get_hash().lookup_item(ordered_truck_list[-1])[1][1]].get('Index'))
            min_dist = float('inf')  # Set the minimum distance to infinity
            min_dist_index = ''
            min_dist_package_id = ''

            # Iterate over each package index (all packages going to the same delivery address are the same index) for
            # the given truck in the distance table to find the shortest distance to the next available delivery
            # address.
            for package_index in range(len(package_index_list)):

                # Searching for the lowest value/distance by traversing the distance list horizontally
                if package_row_index > package_index_list[package_index]:
                    if distances[package_row_index][package_index_list[package_index]] != '':
                        if float(distances[package_row_index][package_index_list[package_index]]) < min_dist:
                            if package_index_list[package_index] not in self.addresses:
                                min_dist = float(distances[package_row_index][package_index_list[package_index]])
                                min_dist_index = package_index_list[package_index]
                                min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]
                                min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

                # Searching for the lowest value/distance by traversing the distance list vertically
                elif package_row_index < package_index_list[package_index]:
                    if distances[package_index_list[package_index]][package_row_index] != '':
                        if float(distances[package_index_list[package_index]][package_row_index]) < min_dist:
                            if package_index_list[package_index] not in self.addresses:
                                min_dist = float(distances[package_index_list[package_index]][package_row_index])
                                min_dist_index = package_index_list[package_index]
                                min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]
                                min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

            # print(f'min_dist is: {min_dist}')
            # print(f'min_dist_package_id is: {min_dist_package_id}')

            # Iterating over each package going to the same delivery address.
            for package_num in min_dist_package_id:

                # If the package is the first or only package that is going to the delivery address.
                if package_num == 1:
                    delivery_time_seconds = self.calculate_delivery_time(min_dist)
                    delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                    time_sum = wtime.add_time(delivery_time, delivery_times_list[-1])
                    time_sum_converted = wtime.convert_int_seconds_to_string_time(time_sum)
                    delivery_times_list.append(time_sum_converted)  # [O(n)]
                    total_truck_dist.append(min_dist)

                # If the package is not the first package going to the delivery address.
                else:
                    time_sum = wtime.add_time('00:00:00', delivery_times_list[-1])
                    time_sum_converted = wtime.convert_int_seconds_to_string_time(time_sum)
                    delivery_times_list.append(time_sum_converted)  # [O(n)]
                    total_truck_dist.append(0.0)

                ordered_truck_list.append(min_dist_package_id[package_num])

                # print(f'\nPackage ID is: {min_dist_package_id[package_num]}')

                # delivery_times_list.append(time_sum_converted)  # [O(n)]
                # total_truck_dist.append(min_dist)
                # ordered_truck_list.append(min_dist_package_id[package_num])
                # self.addresses.append(min_dist_index)
                # packages += 1

                # print(f'packages is: {packages}')

            if min_dist_index != '':
                self.addresses.append(min_dist_index)

            # if len(ordered_truck_list) == len(package_list):
            #     break

            packages += 1

        # Calculate and append the time and distance to get back to the hub from the last delivery.
        return_to_hub = float(ppd.get_distance_data()[int(record_data.get(ppd.get_input_data()[ordered_truck_list[-1] - 1][1])["Index"])][0])  # [O(1)]
        delivery_time_seconds = self.calculate_delivery_time(return_to_hub)
        delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
        delivery_times_list.append(wtime.convert_int_seconds_to_string_time(
            wtime.add_time(delivery_time, delivery_times_list[-1])))  # [O(n)]
        total_truck_dist.append(return_to_hub)
        if min_dist_index != '':
            self.addresses.append(min_dist_index)
        package_list = ordered_truck_list

        print(f'Truck {truck_num + 1}({len(package_list)}): {package_list}')

        adjusted_package_list = self.check_truck_times(ordered_truck_list, delivery_times_list, record_data)

        # Calling the find_shortest_distance method if the package_list was adjusted and passing in the
        # adjusted_package_list

        # XXXXXXXXXX Try to recalculate/re-append the delivery times and distances. XXXXXXXXXX

        if not adjusted_package_list[1]:
            while not adjusted_package_list[1]:
                # print(f'delivery_times_list is: {delivery_times_list}')
                self.addresses = list(set(self.addresses).difference(set(package_index_list)))
                # self.find_shortest_distance(distances, adjusted_package_list[0], truck_num, record_data)

                delivery_times_list.clear()
                total_truck_dist.clear()

                adjusted_package_index_list = []

                for adjusted_package in adjusted_package_list[0]:
                    adjusted_package_index = int(record_data.get(ppd.get_hash().lookup_item(adjusted_package)[1][1])['Index'])
                    if adjusted_package_index not in adjusted_package_index_list:
                        adjusted_package_index_list.append(adjusted_package_index)

                print(f'adjusted_package_index_list is: {adjusted_package_index_list}')

                # Iterating over each package going to the same delivery address.
                for adjusted_package_num in range(len(adjusted_package_index_list)):

                    print(f'adjusted_package_num is: {adjusted_package_num}')



                    # If the package is the first or only package that is going to the delivery address.
                    if adjusted_package_num == 1:
                        delivery_time_seconds = self.calculate_delivery_time(dist)
                        delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
                        time_sum = wtime.add_time(delivery_time, delivery_times_list[-1])
                        time_sum_converted = wtime.convert_int_seconds_to_string_time(time_sum)
                        delivery_times_list.append(time_sum_converted)  # [O(n)]
                        total_truck_dist.append(min_dist)

                    # If the package is not the first package going to the delivery address.
                    else:
                        print(f'delivery_times_list is: {delivery_times_list}')

                        time_sum = wtime.add_time('00:00:00', delivery_times_list[-1])
                        time_sum_converted = wtime.convert_int_seconds_to_string_time(time_sum)
                        delivery_times_list.append(time_sum_converted)  # [O(n)]
                        total_truck_dist.append(0.0)

                print(delivery_times_list)
                adjusted_package_list = self.check_truck_times(ordered_truck_list, delivery_times_list, record_data)
            ordered_truck_list = adjusted_package_list[0]

        # Assign the value of the distances and delivery times to the appropriate truck.
        if truck_num == 0:  # Truck 1
            self.total_dist_first_truck = total_truck_dist
            self.first_truck_delivery_times = delivery_times_list
            self.first_truck = ordered_truck_list
            self.delivery_data.append([self.first_truck, self.first_truck_delivery_times])
            print(f'Truck 1: {self.total_dist_first_truck}')
            print(f'Truck 1: {self.first_truck_delivery_times}')
        if truck_num == 1:  # Truck 2
            self.total_dist_second_truck = total_truck_dist
            self.second_truck_delivery_times = delivery_times_list
            self.second_truck = ordered_truck_list
            self.delivery_data.append([self.second_truck, self.second_truck_delivery_times])
            print(f'Truck 2: {self.total_dist_second_truck}')
            print(f'Truck 2: {self.second_truck_delivery_times}')
        if truck_num == 2:  # Truck 3
            self.total_dist_third_truck = total_truck_dist
            self.third_truck_delivery_times = delivery_times_list
            self.third_truck = ordered_truck_list
            self.delivery_data.append([self.third_truck, self.third_truck_delivery_times])
            print(f'Truck 3: {self.total_dist_third_truck}')
            print(f'Truck 3: {self.third_truck_delivery_times}')

        # Assign the truck list back to the original list after it\'s been rearranged.
        # self.first_truck = package_list[0]
        # self.second_truck = package_list[1]
        # self.third_truck = package_list[2]

        # print(f'self.first_truck_delivery_times is: {self.first_truck_delivery_times}')
        # print(f'self.second_truck_delivery_times is: {self.second_truck_delivery_times}')
        # print(f'self.third_truck_delivery_times is: {self.third_truck_delivery_times}')
        #
        # self.delivery_data.append([self.first_truck, self.first_truck_delivery_times])
        # self.delivery_data.append([self.second_truck, self.second_truck_delivery_times])
        # self.delivery_data.append([self.third_truck, self.third_truck_delivery_times])

        self.print_verbose_output()

        return package_list

    @staticmethod
    def check_truck_times(package_id_list, delivery_time_list, record_data):

        # print(f'\npackage_list is: {package_id_list}')

        move_candidates = []
        delivery_window = True

        for package_id_list_index in range(len(package_id_list)):
            # print(f'\npackage_id_list_index is: {package_id_list_index}')
            # print(f'package_id_list[package_id_list_index] is: {package_id_list[package_id_list_index]}')
            # print(f'delivery_time_list[package_id_list_index] is: {delivery_time_list[package_id_list_index]}')

            deliver_by = record_data[ppd.get_hash().lookup_item(package_id_list[package_id_list_index])[1][1]]['Deliver By']
            try:
                delayed_eta = record_data[ppd.get_hash().lookup_item(package_id_list[package_id_list_index])[1][1]]['Delayed ETA']
            except KeyError:
                delayed_eta = None

            # print(f'delayed_eta is: {delayed_eta}')
            # print(f'deliver_by is: {deliver_by}')

            if delayed_eta is None and deliver_by == 'EOD':
                if delivery_window:
                    delivery_window = True
                move_candidates.append([package_id_list_index, package_id_list[package_id_list_index], float(ppd.get_distance_data()[int(record_data.get(ppd.get_input_data()[package_id_list[package_id_list_index]][1])["Index"])][0])])  # [O(1)]
                # print(f'Appending Package Index: {package_id_list_index}, Package ID: {package_id_list[package_id_list_index]}, and Distance to Hub: {float(ppd.get_distance_data()[int(record_data.get(ppd.get_input_data()[package_id_list[package_id_list_index]][1])["Index"])][0])} to move_candidates.')
                # print(f'Package ID {min_dist_package_id[package_num]} is not delayed and needs to be delivered by EOD')

            elif delayed_eta is None and deliver_by != 'EOD':
                deliver_by_diff = wtime.time_difference(deliver_by, delivery_time_list[package_id_list_index])
                if deliver_by_diff >= 0:
                    # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is on or before {deliver_by}')
                    if delivery_window:
                        delivery_window = True
                else:
                    # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is after {deliver_by}')
                    delivery_window = False

            elif delayed_eta is not None and deliver_by == 'EOD':
                delayed_eta_diff = wtime.time_difference(delivery_time_list[package_id_list_index], delayed_eta)
                if delayed_eta_diff >= 0:
                    # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is on or after {delayed_eta}')
                    if delivery_window:
                        delivery_window = True
                else:
                    # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is before {delayed_eta}')
                    delivery_window = False

            else:
                deliver_by_diff = wtime.time_difference(deliver_by, delivery_time_list[package_id_list_index])
                delayed_eta_diff = wtime.time_difference(delivery_time_list[package_id_list_index], delayed_eta)
                if delayed_eta_diff >= 0 and deliver_by_diff >= 0:
                    # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is on or after {delayed_eta} and on or before {deliver_by}')
                    if delivery_window:
                        delivery_window = True
                else:
                    if deliver_by_diff >= 0:
                        # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is before {delayed_eta}, but on or before {deliver_by}')
                        if delivery_window:
                            delivery_window = True
                    if delayed_eta_diff >= 0:
                        # print(f'Package ID {min_dist_package_id[package_num]} was delivered at {time_sum_converted}, which is on or after {delayed_eta}, but after {deliver_by}')
                        delivery_window = False

        # print(f'delivery_window is: {delivery_window}')
        # print(f'time_sum_converted is: {time_sum_converted}')
        # print(f'min_dist_value is: {min_dist_value}')
        # print(f'move_candidates is: {move_candidates}')
        # If the required "Deliver By" and "Delayed ETA" conditions have been met.
        if not delivery_window:

            min_dist_from_hub = float('inf')
            # print(f'move_candidates is: {move_candidates}')
            for candidate_dist in move_candidates:
                if candidate_dist[2] < min_dist_from_hub:
                    candidate_index = candidate_dist[0]
                    candidate_id = candidate_dist[1]
                    min_dist_from_hub = candidate_dist[2]

        #     print(f'ordered_truck_list after is: {ordered_truck_list}')
        #     # print(f'min_dist_from_hub is: {min_dist_from_hub}')
        #     print(f'popping package ID {candidate_id} from index {candidate_index} in ordered_truck_list')
        #     print(f'min_dist_index is: {min_dist_index}')
        #     candidate_id = move_candidates[1][1]
        #     candidate_index = move_candidates[1][0]
            print(F'POPPING PACKAGE ID {candidate_id} AT INDEX {candidate_index}')
            package_id_list.pop(candidate_index)
            print(f'APPENDING PACKAGE ID {candidate_index} TO package_id_list.')
            package_id_list.append(candidate_id)
        #     # delivery_times_list.pop(candidate_index)
        #     # total_truck_dist.pop(candidate_index)
        #     candidate_index_popped = True
        #     # self.addresses.append(min_dist_index)
        #     print(f'appending package ID {candidate_id} to the ordered_truck_list')
        #     # ordered_truck_list.append(candidate_id)
        #     print(f'ordered_truck_list after is: {ordered_truck_list}')
        #     continue
        #     # delivery_times_list.append(time_sum_converted)  # [O(n)]
        #     # total_truck_dist.append(min_dist)
        #     # ordered_truck_list.append(min_dist_package_id[package_num])
        #     # continue
        #     # print(min(move_candidates[2]))
        # # else:
        #     # pop the best candidate off and append it back onto the list.

        return [package_id_list, delivery_window]

    @staticmethod
    def calculate_delivery_time(distance):
        """
        This method calculates the time it takes to travel the distance passed in given the constant average speed.

        :parameter distance(float)
        :return: (int)delivery time in seconds.
        """
        return int(distance / DELIVERY_TRUCK_AVG_SPEED_MPH * 3600)

    # Print verbose delivery data
    def print_verbose_output(self):

        truck1_total_distance = round(sum(self.total_dist_first_truck), 2)
        truck2_total_distance = round(sum(self.total_dist_second_truck), 2)
        truck3_total_distance = round(sum(self.total_dist_third_truck), 2)

        # Output the result
        print()
        print('#' * 120)
        print(' ' * 45 + 'All packages have been loaded')
        print('#' * 120)

        print(f'\nTruck 1 Package IDs: {self.first_truck}(# of packages: {len(self.first_truck)},'
              f' Distance: {truck1_total_distance} miles)')
        print(f'Truck 1 Distance List: {self.total_dist_first_truck}(miles)')
        print(f'Truck 1 Delivery Times: {self.first_truck_delivery_times}')
        # print(f'Truck 1 Duration Times: {self.first_truck_delivery_times[0]}')

        print(f'\nTruck 2 Package IDs: {self.second_truck}(# of packages: {len(self.second_truck)},'
              f' Distance: {truck2_total_distance} miles)')
        print(f'Truck 2 Distance List: {self.total_dist_second_truck}(miles)')
        print(f'Truck 2 Delivery Times: {self.second_truck_delivery_times}')
        # print(f'Truck 2 Duration Times: {self.second_truck_delivery_times[0]}')

        print(f'\nTruck 3 Package IDs: {self.third_truck}(# of packages: {len(self.third_truck)},'
              f' Distance: {truck3_total_distance} miles)')
        print(f'Truck 3 Distance List: {self.total_dist_third_truck}(miles)')
        print(f'Truck 3 Delivery Times: {self.third_truck_delivery_times}')
        # print(f'Truck 3 Duration Times: {self.third_truck_delivery_times[0]}')

        total_distance_traveled = round(truck1_total_distance + truck2_total_distance + truck3_total_distance, 2)

        print(f'\nTotal Distance traveled: {total_distance_traveled} miles')
        print('#' * 120)

    # Update package status - [O(n)]
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
                (truck_num == 3 and wtime.time_difference(self.first_truck_delivery_times[-1], lookup_time) > 0)):
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
                print('|', f'Truck {truck_num} left the the hub at {self.first_truck_delivery_times[-1]}'.center(122), '|')

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

        # Iterate over each package and update their status.
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
            first_truck_diff = wtime.time_difference(self.first_truck_delivery_times[delivered_count - 1], FIRST_TRUCK_DEPARTURE_TIME)
            first_truck_diff = wtime.convert_int_seconds_to_string_time(first_truck_diff)

        # Calculate second truck delivery duration
        if truck_num == 2:
            second_truck_diff = wtime.time_difference(self.second_truck_delivery_times[delivered_count - 1], self.second_truck_departure_time)
            second_truck_diff = wtime.convert_int_seconds_to_string_time((second_truck_diff))

        # Calculate third truck delivery duration
        if truck_num == 3:
            # print(f'delivery_count is: {delivered_count}')
            # print(f'self.third_truck_delivery_times[delivered_count - 1] is: {self.third_truck_delivery_times}')
            # print(f'self.first_truck_delivery_times[-1] is: {self.first_truck_delivery_times[-1]}')
            third_truck_diff = wtime.time_difference(self.third_truck_delivery_times[delivered_count - 1], self.first_truck_delivery_times[-1])
            third_truck_diff = wtime.convert_int_seconds_to_string_time(third_truck_diff)

        # Calculate first truck delivery duration
        first_total_truck_diff = wtime.time_difference(self.first_truck_delivery_times[-1], FIRST_TRUCK_DEPARTURE_TIME)
        first_total_truck_diff = wtime.convert_int_seconds_to_string_time(first_total_truck_diff)

        # Calculate second truck delivery duration
        second_total_truck_diff = wtime.time_difference(self.second_truck_delivery_times[-1], self.second_truck_departure_time)
        second_total_truck_diff = wtime.convert_int_seconds_to_string_time(second_total_truck_diff)

        # Calculate third truck delivery duration
        third_total_truck_diff = wtime.time_difference(self.third_truck_delivery_times[-1], self.first_truck_delivery_times[-1])
        third_total_truck_diff = wtime.convert_int_seconds_to_string_time(third_total_truck_diff)

        # If the truck has returned to the hub
        if truck_status == truck_status_options[2]:

            if truck_num == 1:
                print('|', f'Truck 1 Summary: {len(self.first_truck)} packages were delivered in {first_total_truck_diff} and traveled {round(sum(self.total_dist_first_truck), 2)} miles.'.center(122), '|')

            if truck_num == 2:
                print('|', f'Truck 2 Summary: {len(self.second_truck)} packages were delivered in {second_total_truck_diff} and traveled {round(sum(self.total_dist_second_truck), 2)} miles.'.center(122), '|')

            if truck_num == 3:
                print('|', f'Truck 3 Summary: {len(self.third_truck)} packages were delivered in {third_total_truck_diff} and traveled {round(sum(self.total_dist_third_truck), 2)} miles.'.center(122), '|')

        # If the truck is currently delivering packages.
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

        # The truck is still at the hub and has not started delivering packages yet.
        else:
            print('|', f'Truck {truck_num} has not left the hub yet.'.center(122), '|')

        print('-' * 126)

        # All packages have been delivered and all trucks have returned to the hub
        # Calculate the total sum that all trucks traveled to deliver all of the packages.
        self.total_distance_traveled = round(
            sum(self.total_dist_first_truck) +
            sum(self.total_dist_second_truck) +
            sum(self.total_dist_third_truck), 2
        )

        # Calculate the total time it took for all of the packages to be delivered.
        self.total_delivery_time = (
                wtime.convert_string_time_to_int_seconds(first_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(second_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(third_total_truck_diff)
        )

        self.total_delivery_time = wtime.convert_int_seconds_to_string_time(self.total_delivery_time)

        # Print output of the total distance traveled and the total time it took to deliver all packages.
        if truck_num == 3:
            print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
            print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

    def update_package_delivery_status_and_print_output_for_single_package(
            self,
            truck_list,
            truck_num,
            delivery_time_list,
            lookup_time,
            **kwargs
    ):

        delivered_count = 0
        first_truck_diff = 0
        second_truck_diff = 0
        third_truck_diff = 0
        truck_status_options = ['At the hub', 'Delivering packages', 'Returned to the hub']
        package_status_options = ['At the hub', 'En route', 'Delivered']
        value_index = 6  # The package status index

        package_id = kwargs['package_id']
        package_index = kwargs['package_index']

        # If user entered look up time is prior to the truck leaving the hub
        if ((truck_num == 1 and wtime.time_difference(FIRST_TRUCK_DEPARTURE_TIME, lookup_time) > 0) or
                (truck_num == 2 and wtime.time_difference(self.second_truck_departure_time, lookup_time) > 0) or
                (truck_num == 3 and wtime.time_difference(self.first_truck_delivery_times[-1], lookup_time) > 0)):
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
                print('|', f'Truck {truck_num} left the the hub at {self.first_truck_delivery_times[-1]}'.center(122), '|')

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

        package_id_loop = 0

        # for package_index in range(len(truck_list) + 1):
        #
        #     if package_index >= len(truck_list):
        #         continue
        #
        #     # Padding the single digits with a leading space for prettier output
        #     if truck_list[package_index] < 10:
        #         package_id_loop = f' {str(truck_list[package_index])}'
        #     else:
        #         package_id_loop = str(truck_list[package_index])

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
            first_truck_diff = wtime.time_difference(self.first_truck_delivery_times[delivered_count - 1], FIRST_TRUCK_DEPARTURE_TIME)
            first_truck_diff = wtime.convert_int_seconds_to_string_time(first_truck_diff)

        # Calculate second truck delivery duration
        if truck_num == 2:
            second_truck_diff = wtime.time_difference(self.second_truck_delivery_times[delivered_count - 1], self.second_truck_departure_time)
            second_truck_diff = wtime.convert_int_seconds_to_string_time((second_truck_diff))

        # Calculate third truck delivery duration
        if truck_num == 3:
            third_truck_diff = wtime.time_difference(self.third_truck_delivery_times[delivered_count - 1], self.first_truck_delivery_times[-1])
            third_truck_diff = wtime.convert_int_seconds_to_string_time(third_truck_diff)

        # Calculate first truck delivery duration
        first_total_truck_diff = wtime.time_difference(self.first_truck_delivery_times[-1], FIRST_TRUCK_DEPARTURE_TIME)
        first_total_truck_diff = wtime.convert_int_seconds_to_string_time(first_total_truck_diff)

        # Calculate second truck delivery duration
        second_total_truck_diff = wtime.time_difference(self.second_truck_delivery_times[-1], self.second_truck_departure_time)
        second_total_truck_diff = wtime.convert_int_seconds_to_string_time(second_total_truck_diff)

        # Calculate third truck delivery duration
        third_total_truck_diff = wtime.time_difference(self.third_truck_delivery_times[-1], self.first_truck_delivery_times[-1])
        third_total_truck_diff = wtime.convert_int_seconds_to_string_time(third_total_truck_diff)

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
                wtime.convert_string_time_to_int_seconds(first_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(second_total_truck_diff) +
                wtime.convert_string_time_to_int_seconds(third_total_truck_diff)
        )

        self.total_delivery_time = wtime.convert_int_seconds_to_string_time(self.total_delivery_time)

        # Print output if truck 3 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[-1], self.second_truck_delivery_times[-1]) >= 0:
            if truck_status == truck_status_options[2] and truck_num == 3:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')

        # Print output if truck 2 is the last truck to complete deliveries
        if wtime.time_difference(self.third_truck_delivery_times[-1], self.second_truck_delivery_times[-1]) <= 0:
            if truck_status == truck_status_options[2] and truck_num == 2:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles')
                print(f'Total time trucks were delivering packages: {self.total_delivery_time} (HH:MM:SS)')
