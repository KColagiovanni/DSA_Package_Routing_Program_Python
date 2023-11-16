from parse_package_data import Packages
from hash_table import HashTable
from wgups_time import WgupsTime

DELIVERY_TRUCK_AVG_SPEED_MPH = 18
FIRST_TRUCK_DEPARTURE_TIME = '8:00:00'
MAX_PACKAGES_PER_TRUCK = 16
TABLE_SIZE = 40

ppd = Packages()
ht = HashTable(TABLE_SIZE)
wtime = WgupsTime()


class DeliverPackages:
    """
    This class handles the loading of trucks and delivery pf packages. The packages get manually loaded onto the trucks
    based on their requirements. Then a greedy algorithm finds the shortest distances between each package. Finally, the
    package status' are updated based on the time entered by the user and the data is printed to the console.

    Attributes: None
    """

    def __init__(self):
        """
        Initializes the variables that will be used throughout the class.

        Parameters:
            self.first_truck(list): The package ID's of each package on the first truck.
            self.first_truck_delivery_times(list): The time each package on the first truck was delivered. The last time
            in this list is the time that the truck returned to the hub.
            self.total_dist_first_truck(list): The distance the first truck traveled between the hub and the first
            package, then to each following package, and finally from the last package to the hub.

            self.second_truck(list): The package ID's of each package on the second truck.
            self.second_truck_delivery_times(list): The time each package on the second truck was delivered. The last
            time in this list is the time that the truck returned to the hub.
            self.total_dist_second_truck(list): The distance the second truck traveled between the hub and the first
            package, then to each following package, and finally from the last package to the hub.

            self.third_truck(list): The package ID's of each package on the third truck.
            self.third_truck_delivery_times(list): The time each package on the third truck was delivered. The last time
            in this list is the time that the truck returned to the hub.
            self.total_dist_third_truck(list): The distance the third truck traveled between the hub and the first
            package, then to each following package, and finally from the last package to the hub.

            self.addresses(list): The index of each package that has been loaded. Index 0 is initialized into this list
            because it is the hub.
            self.been_loaded(list): Package ID's of packages that have been loaded.
            self.candidate_tried(list): Candidate package ID's of packages that were added as possible candidates when
            adjusting loaded packages.
            self.delivery_data(list): A 2d list containing the package ID's and the package delivery times.
            self.distance_traveled(list): Times each package was delivered.
            self.truck_list(list): A 2d list containing the package ID's on each truck.

            self.move_candidates(set): The package ID's of each possible candidate package to use when adjusting the
            list.
            self.packages_to_be_delivered_together(set): The package ID's of the packages that need to all be on the
            same truck.

            self.second_truck_departure_time(str): The departure time of the second truck, which is defined as the
            earliest "delayed" package time.
            self.total_distance_traveled(float): The sum of the distance, in miles, that all trucks have traveled.
            self.total_delivery_time(str): The total delivery time for all packages in string (HH:MM:SS) format.
            self.total_packages_loaded(int): A counter variable to keep track of the number of packages that have been
            loaded when manually loading trucks.

        Returns: None
        """
        self.first_truck = []
        self.first_truck_delivery_times = []
        self.total_dist_first_truck = []

        self.second_truck = []
        self.second_truck_delivery_times = []
        self.total_dist_second_truck = []

        self.third_truck = []
        self.third_truck_delivery_times = []
        self.total_dist_third_truck = []

        self.addresses = [0]
        self.been_loaded = []
        self.candidate_tried = []
        self.delivery_data = []
        self.distance_traveled = []
        self.total_delivery_time = []
        self.truck_list = []

        self.move_candidates = set()
        self.packages_to_be_delivered_together = set()

        self.second_truck_departure_time = ''
        self.total_packages_loaded = 0
        self.total_distance_traveled = 0.0

    def load_package_onto_first_truck(self, package_id):
        """
        This method loads packages onto the first truck. It first checks if the truck has room for all the packages
        that will be going to the same address, then loads each package going to the same address. Finally, it checks
        that the package(s) has(have) not been loaded already, then appends them to the truck.

        Time Complexity: O(n)

        Parameters: 
            package_id(dict): A dict of the package(s) that are going to the same address. With the package number as
            the key and the package ID as the value (Ex: {1: 15, 2: 16, 3: 34}).

        Returns: False if the truck is fullm otherwise None is returned.
        """
        if len(self.first_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)]
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.first_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1
        return False

    def load_package_onto_second_truck(self, package_id):
        """
        This method loads packages onto the second truck. It first checks if the truck has room for all the packages
        that will be going to the same address, then loads each package going to the same address. Finally, it checks
        that the package(s) has(have) not been loaded already, then appends them to the truck.

        Time Complexity: O(n)

        Parameters: 
            package_id(dict): A dict of the package(s) that are going to the same address. With the package number as
            the key and the package ID as the value (Ex: {1: 15, 2: 16, 3: 34}).

        Returns: False if the truck is fullm otherwise None is returned.
        """
        if len(self.second_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)] This wont changed with a bigger data set
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.second_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1
        return False

    def load_package_onto_third_truck(self, package_id):
        """
        This method loads packages onto the third truck. It first checks if the truck has room for all the packages
        that will be going to the same address, then loads each package going to the same address. Finally, it checks
        that the package(s) has(have) not been loaded already, then appends them to the truck.

        Time Complexity: O(n)

        Parameters: 
            package_id(dict): A dict of the package(s) that are going to the same address. With the package number as
            the key and the package ID as the value (Ex: {1: 15, 2: 16, 3: 34}).

        Returns: False if the truck is fullm otherwise None is returned.
        """
        if len(self.third_truck) + len(package_id) < MAX_PACKAGES_PER_TRUCK:
            for package_num in package_id:  # [O(3) ==> O(1)] This wont changed with a bigger data set
                if package_id[package_num] not in self.been_loaded:  # [O(n)]
                    self.third_truck.append(package_id[package_num])
                    self.been_loaded.append(package_id[package_num])
                    self.total_packages_loaded += 1
        return False

    def manual_load(self, record_data):
        """
        This method manually loads the packages onto the trucks based on their requirements.

        Time Complexity: O(n^2)

        Parameters: 
            record_data(dict): This is data from the package data csv file and distance data csv files that has
            information for each delivery address to help load the trucks.

        Returns:
            self.truck_list(list): A list of nested lists of package ID's for each truck.
        """
        # Adding the packages that must be on the same truck to a list.
        for record in record_data:  # [O(n)]
            deliver_together = record_data[record].get('Deliver Together')
            if deliver_together is not None:
                self.packages_to_be_delivered_together = deliver_together

        # Loading the packages that must go on the same truck together,prior to loading the rest of the packages.
        for package in self.packages_to_be_delivered_together:  # [O(n^2)]

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
                self.load_package_onto_first_truck(package_id_data)  # [O(n)]

            # Must be on first truck
            if truck == 1:
                self.load_package_onto_first_truck(package_id_data)  # [O(n)]

            # Must be on second truck
            if truck == 2:
                self.load_package_onto_second_truck(package_id_data)  # [O(n)]

            # Must be on third truck
            if truck == 3:
                self.load_package_onto_third_truck(package_id_data)  # [O(n)]

            if deliver_by_time != 'EOD':
                # Truck 1
                if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                    self.load_package_onto_first_truck(package_id_data)  # [O(n)]

                # Truck 2
                if self.second_truck_departure_time != '':
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        self.load_package_onto_second_truck(package_id_data)  # [O(n)]

            # Truck 3
            else:
                self.load_package_onto_third_truck(package_id_data)  # [O(n)]

        # Load packages onto trucks that they are required to be on.
        for record in record_data:  # [O(n^2)]

            truck = record_data[record].get('Truck')  # [O(1)]
            package_id_data = record_data[record].get('Package ID')  # [O(1)]

            if truck is not None:

                # Load onto first truck
                if truck == 1:
                    self.load_package_onto_first_truck(package_id_data)  # [O(n)]

                # Load onto second truck
                if truck == 2:
                    self.load_package_onto_second_truck(package_id_data)  # [O(n)]

                # Load onto third truck
                if truck == 3:
                    self.load_package_onto_third_truck(package_id_data)  # [O(n)]

        # Determine which truck each package needs to be loaded onto based on whether it's delayed or not.
        for record in record_data:  # [O(n^2)]

            delayed_package = record_data[record].get('Delayed ETA')  # [O(1)]
            package_id_data = record_data[record].get('Package ID')  # [O(1)]
            deliver_by_time = record_data[record].get('Deliver By')  # [O(1)]

            if delayed_package is not None:

                # Truck 2
                if self.second_truck_departure_time == '':
                    self.second_truck_departure_time = delayed_package

                # Truck 3
                if deliver_by_time == 'EOD' and len(package_id_data) < 2:
                    self.load_package_onto_third_truck(package_id_data)  # [O(n)]

                if wtime.time_difference(self.second_truck_departure_time, delayed_package) >= 0:
                    self.second_truck_departure_time = delayed_package
                    self.load_package_onto_second_truck(package_id_data)  # [O(n)]

        # Determine which truck each package needs to be on based on it's "deliver by" time.
        for record in record_data:  # [O(n^2)]
            deliver_by_time = record_data[record].get('Deliver By')  # [O(1)]
            package_id_data = record_data[record].get('Package ID')  # [O(1)]

            if deliver_by_time is not None:

                if deliver_by_time != 'EOD':

                    # If deliver by time is after the departure time of the first truck
                    if wtime.time_difference(deliver_by_time, FIRST_TRUCK_DEPARTURE_TIME) > 0:
                        self.load_package_onto_first_truck(package_id_data)  # [O(n)]

                    # If deliver by time is after the departure time of the second truck
                    if wtime.time_difference(deliver_by_time, self.second_truck_departure_time) > 0:
                        self.load_package_onto_second_truck(package_id_data)  # [O(n)]

                # Truck 3
                else:
                    # If deliver by time is "EOD" and truck 3 is not full
                    if len(self.third_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_third_truck(package_id_data)  # [O(n)]

                    # If deliver by time is "EOD" and truck 3 is full, but truck 2 is not full
                    elif len(self.second_truck) + len(package_id_data) < MAX_PACKAGES_PER_TRUCK:
                        self.load_package_onto_second_truck(package_id_data)  # [O(n)]

                    # If deliver by time is "EOD" and trucks 2 and 3 are full, but truck 1 is not full
                    else:
                        self.load_package_onto_first_truck(package_id_data)  # [O(n)]

        self.truck_list = [self.first_truck, self.second_truck, self.third_truck]

        return self.truck_list

    def find_shortest_distance(self, distances, package_list, truck_num, record_data):
        """
        This method is the greedy algorithm that rearranges the packages in each manually loaded truck. It first finds
        the package that has the shortest distance to the hub and appends that as the first package. Then it iterates
        through the remaining packages on the truck and finds the shortest distance between the last package that was
        loaded to the remaining packages until all packages have been iterated through. Each time a package is appended,
        the distance is also appended to a separate list and the travel time is calculated, based on the distance and
        the average speed that the trucks travel, and that is also appended to a separate list.

        Time Complexity: O(n^2)

        Parameters:
            distances(list): A 2D list of distances between each delivery address.
            package_list(list): A list of the package_id's that have been manually loaded onto the truck.
            truck_num(int): The truck number of the truck that is holding the packages on the package_list.
            record_data(dict): This is data from the package data csv file and distance data csv files that has
            information for each delivery address to help load the trucks.

        Returns:
            ordered_truck_list(list): The new package_list after it has been rearranged by the greedy algorithm.
        """
        delivery_times_list = []
        min_dist = float('inf')
        min_dist_index = ''
        min_dist_package_address = ''
        ordered_truck_list = []
        package_index_list = []
        total_truck_dist = []

        # Find the package that is closest to the hub.
        for package in package_list:  # [O(n)]
            package_address = ppd.get_hash().lookup_item(package)[1][1]  # [O(1)]
            package_index_in_record_data = int(record_data[package_address].get('Index'))  # [O(1)]
            if float(distances[package_index_in_record_data][0]) < min_dist:
                min_dist = float(distances[package_index_in_record_data][0])
                min_dist_package_address = package_address
                min_dist_index = package_index_in_record_data

        # Append package addresses that are being loaded onto the "address list".
        self.addresses.append(min_dist_index)

        # Add the first package to the first position in the truck and calculate the delivery time.
        for package_num in record_data[min_dist_package_address].get('Package ID'):  # [O(n)]
            package_id = record_data[min_dist_package_address].get('Package ID')[package_num]  # [O(1)]
            ordered_truck_list.append(package_id)

            # If there are multiple packages going to the same address, package 1 will be the first.
            if package_num == 1:
                delivery_time_seconds = self.calculate_delivery_time(min_dist)  # [O(1)]
                delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)  # [O(1)]

                if truck_num == 0:
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(
                        wtime.add_time(delivery_time, FIRST_TRUCK_DEPARTURE_TIME)
                    ))  # [O(1)]
                elif truck_num == 1:
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(
                        wtime.add_time(delivery_time, self.second_truck_departure_time)
                    ))  # [O(1)]
                elif truck_num == 2 and len(self.first_truck_delivery_times) > 0:
                    delivery_times_list.append(wtime.convert_int_seconds_to_string_time(
                        wtime.add_time(delivery_time, self.first_truck_delivery_times[-1])
                    ))  # [O(1)]
                else:
                    raise ValueError("This method wasn't designed to handle more than 3 trucks")

                total_truck_dist.append(min_dist)

            # Add subsequent packages that are going to the same address
            else:
                delivery_times_list.append(wtime.convert_int_seconds_to_string_time(wtime.add_time(
                    '00:00:00', delivery_times_list[-1]))
                )  # [O(1)]
                total_truck_dist.append(0.0)

        # Append the indexes of each package (going to the same address) to the truck, starting at index 1 because
        # the first package (index 0) has already been loaded.
        for packages in range(len(package_list)):  # [O(3) ==> O(1)]
            package_row_index = int(record_data[ppd.get_hash().lookup_item(package_list[packages])[1][1]].get('Index'))
            if package_row_index not in package_index_list:  # [O(n)]
                package_index_list.append(package_row_index)

        # Iterate over each package on the truck that has been manually loaded.
        for packages in range(len(package_list)):  # [O(n^2)]

            package_row_index = int(record_data[ppd.get_hash().lookup_item(ordered_truck_list[-1])[1][1]].get('Index'))
            min_dist = float('inf')  # Set the minimum distance to infinity
            min_dist_index = ''
            min_dist_package_id = ''

            # Iterate over each package index (all packages going to the same delivery address are the same index) for
            # the given truck in the distance table to find the shortest distance to the next available delivery
            # address.
            for package_index in range(len(package_index_list)):  # [O(1)] (Worst case is O(16))

                # Searching for the lowest value/distance by traversing the distance list horizontally
                if package_row_index > package_index_list[package_index]:
                    if distances[package_row_index][package_index_list[package_index]] != '':
                        if float(distances[package_row_index][package_index_list[package_index]]) < min_dist:
                            if package_index_list[package_index] not in self.addresses:  # [O(n)]
                                min_dist = float(distances[package_row_index][package_index_list[package_index]])
                                min_dist_index = package_index_list[package_index]
                                min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]  # [O(n)]
                                min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

                # Searching for the lowest value/distance by traversing the distance list vertically
                elif package_row_index < package_index_list[package_index]:
                    if distances[package_index_list[package_index]][package_row_index] != '':
                        if float(distances[package_index_list[package_index]][package_row_index]) < min_dist:
                            if package_index_list[package_index] not in self.addresses:  # [O(n)]
                                min_dist = float(distances[package_index_list[package_index]][package_row_index])
                                min_dist_index = package_index_list[package_index]
                                min_dist_index_address = ppd.get_distance_name_data()[min_dist_index][2]  # [O(n)]
                                min_dist_package_id = record_data[min_dist_index_address].get('Package ID')

            # Iterating over each package going to the same delivery address.
            for package_num in min_dist_package_id:  # [O(3) ==> O(1)]

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

            # Append package addresses that are being loaded onto the "address list".
            if min_dist_index != '':
                self.addresses.append(min_dist_index)

            packages += 1

        # Calculate and append the time and distance to get back to the hub from the last delivery.
        return_to_hub = float(ppd.get_distance_data()[
                                  int(record_data.get(ppd.get_input_data()[ordered_truck_list[-1] - 1][1])["Index"])
                              ][0])  # [O(n)]

        delivery_time_seconds = self.calculate_delivery_time(return_to_hub)
        delivery_time = wtime.convert_int_seconds_to_string_time(delivery_time_seconds)
        delivery_times_list.append(
            wtime.convert_int_seconds_to_string_time(wtime.add_time(delivery_time, delivery_times_list[-1]))
        )
        total_truck_dist.append(return_to_hub)

        # Append package addresses that are being loaded onto the "address list".
        if min_dist_index != '':
            self.addresses.append(min_dist_index)

        # Adjust the package list until it meets the requirements (returns True from check_truck_times).
        while True:  # [O(n)]

            copy_of_ordered_truck_list = ordered_truck_list[:]

            # Check the package list to make sure the that all packages meet the "deliver by" and delayed times
            # requirements.
            time_check = self.check_truck_times(copy_of_ordered_truck_list, delivery_times_list, record_data)

            if not time_check[0]:
                adjusted_package_list = self.adjust_package_list(
                    copy_of_ordered_truck_list,
                    truck_num,
                    time_check[1],
                    time_check[2],
                    time_check[3],
                    record_data
                )

                # If the package list does not meet the "deliver by" or delayed time requirements.
                if truck_num == 0:
                    distance_and_delivery_times = self.get_distances_and_calculate_delivery_times(
                        distances, adjusted_package_list, record_data, FIRST_TRUCK_DEPARTURE_TIME
                    )  # [O(n)]
                    delivery_times_list = distance_and_delivery_times[1]
                elif truck_num == 1:
                    distance_and_delivery_times = self.get_distances_and_calculate_delivery_times(
                        distances, adjusted_package_list, record_data, self.second_truck_departure_time
                    )  # [O(n)]
                    delivery_times_list = distance_and_delivery_times[1]
                elif truck_num == 2 and len(self.first_truck_delivery_times) > 0:
                    distance_and_delivery_times = self.get_distances_and_calculate_delivery_times(
                        distances, adjusted_package_list, record_data, self.first_truck_delivery_times[-1]
                    )  # [O(n)]
                    delivery_times_list = distance_and_delivery_times[1]
                else:
                    raise ValueError("This method wasn't designed to handle more than 3 trucks")

                # Check the package list again after the adjustment to make sure the that all packages meet the "deliver
                # by" and delayed times.
                time_check = self.check_truck_times(adjusted_package_list, delivery_times_list, record_data)

                if time_check[0]:
                    total_truck_dist = distance_and_delivery_times[0]
                    delivery_times_list = distance_and_delivery_times[1]
                    break
                else:
                    continue

            else:
                ordered_truck_list = copy_of_ordered_truck_list[:]
                self.move_candidates.clear()
                break

        # Assign the value of the distances and delivery times to the appropriate truck.
        if truck_num == 0:  # Truck 1
            self.total_dist_first_truck = total_truck_dist
            self.first_truck_delivery_times = delivery_times_list
            self.first_truck = ordered_truck_list
            self.delivery_data.append([self.first_truck, self.first_truck_delivery_times])
        elif truck_num == 1:  # Truck 2
            self.total_dist_second_truck = total_truck_dist
            self.second_truck_delivery_times = delivery_times_list
            self.second_truck = ordered_truck_list
            self.delivery_data.append([self.second_truck, self.second_truck_delivery_times])
        elif truck_num == 2:  # Truck 3
            self.total_dist_third_truck = total_truck_dist
            self.third_truck_delivery_times = delivery_times_list
            self.third_truck = ordered_truck_list
            self.delivery_data.append([self.third_truck, self.third_truck_delivery_times])
        else:
            raise ValueError("This method wasn't designed to handle more than 3 trucks")

        return ordered_truck_list

    def get_distances_and_calculate_delivery_times(self, distances, package_id_list, record_data, truck_departure_time):
        """
        This method does exactly as it's name says. It gets the distance between each package using the distances in the
         distance list and uses those distances to calculate the travel time.

        Time Complexity: O(n)

        Parameters:
            distances(list): A 2D list of distances between each delivery address.
            package_id_list(list): A list of the package_id's that have been manually loaded onto the truck.
            record_data(dict): This is data from the package data csv file and distance data csv files that has
            information for each delivery address to help load the trucks.
            truck_departure_time(str): The departure time of the truck being passed to the method.

        Return(list): A list containing the list of calculated distances and travel times between package addresses.
        """
        new_package_dist_list = []
        new_package_index_list = []
        new_package_delivery_time_list = []

        # Get the index of each package and append it to a list
        for package_id in package_id_list:  # [O(n)]
            new_package_index = record_data.get(ppd.get_hash().lookup_item(package_id)[1][1])['Index']  # [O(1)]
            new_package_index_list.append(int(new_package_index))

        # Get distance from the hub to the address of the first package and use that to calculate the travel time.
        new_package_dist_list.append(float(distances[new_package_index_list[0]][0]))

        seconds = self.calculate_delivery_time(float(distances[new_package_index_list[0]][0]))  # [O(1)]
        delivery_duration = wtime.convert_int_seconds_to_string_time(seconds)
        delivery_time = wtime.add_time(delivery_duration, truck_departure_time)
        delivery_time_converted = wtime.convert_int_seconds_to_string_time(delivery_time)
        new_package_delivery_time_list.append(delivery_time_converted)

        # Iterate through the list and get the distance from each package to the previous one, starting with the second
        # package and stopping at the last package in the list.
        for package_index in range(1, len(new_package_index_list)):  # [O(n)]

            # Traverse the distance list horizontally.
            if new_package_index_list[package_index] > new_package_index_list[package_index - 1]:
                new_package_dist_list.append(float(
                    distances[new_package_index_list[package_index]][new_package_index_list[package_index - 1]]
                ))

            elif new_package_index_list[package_index] == new_package_index_list[package_index - 1]:
                new_package_dist_list.append(0.0)

            # Traverse the distance list vertically.
            else:
                new_package_dist_list.append(float(
                    distances[new_package_index_list[package_index - 1]][new_package_index_list[package_index]]
                ))

            seconds = self.calculate_delivery_time(new_package_dist_list[-1])
            delivery_duration = wtime.convert_int_seconds_to_string_time(seconds)
            delivery_time = wtime.add_time(delivery_duration, new_package_delivery_time_list[-1])
            delivery_time_converted = wtime.convert_int_seconds_to_string_time(delivery_time)
            new_package_delivery_time_list.append(delivery_time_converted)

        # Get distance from the address of the last package to the hub and use that to calculate the travel time.
        new_package_dist_list.append(float(distances[new_package_index_list[-1]][0]))

        seconds = self.calculate_delivery_time(float(distances[new_package_index_list[-1]][0]))  # [O(1)]
        delivery_duration = wtime.convert_int_seconds_to_string_time(seconds)
        delivery_time = wtime.add_time(delivery_duration, new_package_delivery_time_list[-1])
        delivery_time_converted = wtime.convert_int_seconds_to_string_time(delivery_time)
        new_package_delivery_time_list.append(delivery_time_converted)

        # Return a list with the calculated distances as the first index, and the calculated delivery times as the
        # second index.
        return [new_package_dist_list, new_package_delivery_time_list]

    def check_truck_times(self, package_id_list, delivery_time_list, record_data):
        """
        This method checks the packages on each truck to ensure they each meet the "deliver by" and "delayed ETA"
        requirements.

        Time Complexity: O(n)

        Parameters:
            package_id_list(list): A list of the package_id's that have been manually loaded onto the truck.
            delivery_time_list(list): A list of the delivery times
            record_data(dict): This is data from the package data csv file and distance data csv files that has
            information for each delivery address to help load the trucks.

        Return(list):
            A list containing the package ID's(list) and delivery window(bool). If all requirements are met,then
            delivery_window will be True, else False.
        """
        delivery_window = True
        deliver_by_bool = False
        delayed_bool = False
        trouble_package_id = None

        for package_id_list_index in range(len(package_id_list)):  # [O(n)]

            deliver_by = record_data[ppd.get_hash().lookup_item(
                package_id_list[package_id_list_index]
            )[1][1]]['Deliver By']
            try:
                delayed_eta = record_data[ppd.get_hash().lookup_item(
                    package_id_list[package_id_list_index]
                )[1][1]]['Delayed ETA']
            except KeyError:
                delayed_eta = None

            if delayed_eta is None and deliver_by == 'EOD':

                self.move_candidates.add(package_id_list[package_id_list_index])

            elif delayed_eta is None and deliver_by != 'EOD':
                deliver_by_diff = wtime.time_difference(deliver_by, delivery_time_list[package_id_list_index])
                if deliver_by_diff < 0:
                    delivery_window = False
                    deliver_by_bool = True
                    trouble_package_id = package_id_list[package_id_list_index]

            elif delayed_eta is not None and deliver_by == 'EOD':
                delayed_eta_diff = wtime.time_difference(delivery_time_list[package_id_list_index], delayed_eta)
                if delayed_eta_diff < 0:
                    delivery_window = False
                    delayed_bool = True
                    trouble_package_id = package_id_list[package_id_list_index]

            else:
                deliver_by_diff = wtime.time_difference(deliver_by, delivery_time_list[package_id_list_index])
                delayed_eta_diff = wtime.time_difference(delivery_time_list[package_id_list_index], delayed_eta)
                if deliver_by_diff < 0 or delayed_eta_diff < 0:
                    delivery_window = False
                    deliver_by_bool = True
                    delayed_bool = True
                    trouble_package_id = package_id_list[package_id_list_index]

        return [delivery_window, deliver_by_bool, delayed_bool, trouble_package_id]

    def adjust_package_list(
            self, package_id_list, truck_num, deliver_by_bool, delayed_bool, trouble_package_id, record_data
    ):
        """
        This method checks the package list for "candidate" packages, which are chosen based on the fact that they
        don't have a delayed time and deliver by is EOD, since they can be in any position on the truck without penalty.

        Time Complexity: O(n^2)

        Parameters:
            package_id_list(list): A list of the package_id's.
            truck_num(int): The truck (1, 2, or 3) that is being adjusted.

        Returns:
            package_id_list(list): The package id list after it's been adjusted.
        """
        if self.candidate_tried != list(self.move_candidates):
            for candidate_package_id in range(len(self.move_candidates)):  # [O(n)] (Worst case)
                if list(self.move_candidates)[candidate_package_id] not in self.candidate_tried:  # [O(n)]]
                    if list(self.move_candidates)[candidate_package_id] != package_id_list[-1]:
                        self.candidate_tried.append(list(self.move_candidates)[candidate_package_id])
                        package_id_list.remove(list(self.move_candidates)[candidate_package_id])  # [O(n)]]
                        package_id_list.append(list(self.move_candidates)[candidate_package_id])

                        return package_id_list
        else:
            package_id_list.remove(trouble_package_id)

            troubled_package_id_address = ppd.get_hash().lookup_item(trouble_package_id)[1][1]
            truck = record_data[troubled_package_id_address].get('Truck')  # [O(1)]
            deliver_together = record_data[troubled_package_id_address].get('Deliver Together')

            if truck_num == 0:
                if deliver_by_bool:
                    package_id_list.insert(0, trouble_package_id)
                elif truck is None and deliver_together is None:
                    if delayed_bool:
                        self.third_truck.append(trouble_package_id)

            if truck_num == 1:
                if deliver_by_bool:
                    package_id_list.insert(0, trouble_package_id)
                elif truck is None and deliver_together is None:
                    if delayed_bool:
                        self.third_truck.append(trouble_package_id)

            if truck_num == 2:
                if deliver_by_bool and truck is None and deliver_together is None:
                    self.first_truck.append(trouble_package_id)
                else:
                    if delayed_bool:
                        package_id_list.append(trouble_package_id)

    @staticmethod
    def calculate_delivery_time(distance):
        """
        This method calculates the time it takes to travel the distance passed in given the constant average speed.

        Time Complexity: O(1)

        Paameters: distance(float): The distance in miles.

        Return(int): Calculated delivery time in seconds.
        """
        return int(distance / DELIVERY_TRUCK_AVG_SPEED_MPH * 3600)

    def update_package_delivery_status_and_print_output(
            self,
            truck_list,
            truck_num,
            delivery_time_list,
            lookup_time,
            **kwargs
    ):
        """
        This method updates the package and truck status' based on the lookup time passed in by the user. The package
        status options are: "At the hub", "En Route", or "Delivered at HH:MM:SS". The truck status options are: "At the
        hub", "Delivering packages", or "Returned to the hub". Then the status' and package info are printed to the
        console.

        Time Complexity: O(n)

        Parameters
            truck_list(list): A list of nested lists of package ID's for each truck.
            truck_num(int): The truck number that is being analyzed.
            delivery_time_list(list): A list of the delivery times for each truck.
            lookup_time(str): The time that the user entered to see package information.
            kwargs: (This is only used when the used chooses option 2.)
                package_id(str): The package ID that the user entered to have info shown for.
                package_index(int): The index in the truck list of the package.
                single_package_lookup(bool): True if this will just be displaying info for one truck and False if it
                will be displaying ingo for all trucks.

        Returns: None
        """
        delivered_count = 0
        first_truck_diff = 0
        second_truck_diff = 0
        third_truck_diff = 0
        truck_status_options = ['At the hub', 'Delivering packages', 'Returned to the hub']
        package_status_options = ['At the hub', 'En route', 'Delivered']

        # kwargs that are used when the user chooses option 2.
        package_id = kwargs['package_id']
        package_index = kwargs['package_index']
        single_package_lookup = kwargs['single_package_lookup']

        value_index = 6  # The package status index

        # If user entered look up time is prior to the truck leaving the hub.
        if ((truck_num == 1 and wtime.time_difference(FIRST_TRUCK_DEPARTURE_TIME, lookup_time) > 0) or
                (truck_num == 2 and wtime.time_difference(self.second_truck_departure_time, lookup_time) > 0) or
                (truck_num == 3 and wtime.time_difference(self.first_truck_delivery_times[-1], lookup_time) > 0)):
            truck_status = truck_status_options[0]

        # If user entered time is past the time that the truck has returned to the hub.
        elif wtime.time_difference(lookup_time, delivery_time_list[-1]) > 0:
            truck_status = truck_status_options[2]

        # If the user entered time is after the truck left the hub, but before it has returned.
        else:
            truck_status = truck_status_options[1]

        print('\n\n')
        print('-' * 126)

        # If the truck is either currently delivering packages or already returned to the hub.
        if truck_status == truck_status_options[1] or truck_status == truck_status_options[2]:

            if truck_num == 1:
                print('|', f'Truck {truck_num} left the the hub at {FIRST_TRUCK_DEPARTURE_TIME}'.center(122),
                      '|')

            if truck_num == 2:
                print('|', f'Truck {truck_num} left the the hub at {self.second_truck_departure_time}'.center(122),
                      '|')

            if truck_num == 3:
                print('|', f'Truck {truck_num} left the the hub at {self.first_truck_delivery_times[-1]}'.center(122),
                      '|')

            # If truck is currently delivering packages.
            if truck_status == truck_status_options[1]:
                print('|', f'Truck {truck_num} status: {truck_status}'.center(122), '|')

            # If truck is not currently delivering packages.
            else:
                print('|', f'Truck {truck_num} status: {truck_status} at {delivery_time_list[-1]}'.center(122), '|')

        # If truck has not left the hub to deliver packages.
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
            '|', 'Status'.center(21),
            '|')

        print('-' * 126)

        # If the user chose to look up a single packager at a specified time.
        if single_package_lookup:

            # If the package has been delivered.
            if wtime.time_difference(lookup_time, delivery_time_list[package_index]) > 0:
                ppd.get_hash().update_item(
                    package_id, value_index, f'{package_status_options[2]} at {delivery_time_list[package_index]}'
                )
                delivered_count += 1

            # If the package is en route.
            elif truck_status == truck_status_options[1]:
                ppd.get_hash().update_item(package_id, value_index, package_status_options[1])

            # If the package is still at the hub.
            else:
                ppd.get_hash().update_item(package_id, value_index, package_status_options[0])

            package_id = ppd.get_hash().lookup_item(package_id)[1][0]

            # Padding the single digits with a leading space for prettier output.
            if int(package_id) < 10:
                package_id = ' ' + package_id

            # Unpacking the hash table entry.
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
                f'| {status}'.ljust(23),
                '|'
            )

        # Else the user chose to look up the info and status' for all packages at a specified time.
        else:

            # Iterate over each package and update their status.
            for package_index in range(len(truck_list) + 1):  # [O(n)]

                if package_index >= len(truck_list):
                    continue

                # Padding the single digits with a leading space for prettier output.
                if truck_list[package_index] < 10:
                    package_id = f' {str(truck_list[package_index])}'
                else:
                    package_id = str(truck_list[package_index])

                # If the package has been delivered.
                if wtime.time_difference(lookup_time, delivery_time_list[package_index]) > 0:
                    ppd.get_hash().update_item(package_id, value_index, f'{package_status_options[2]} at '
                                                                        f'{delivery_time_list[package_index]}')
                    delivered_count += 1

                # If the package is en route.
                elif truck_status == truck_status_options[1]:
                    ppd.get_hash().update_item(package_id, value_index, package_status_options[1])

                # If the package is still at the hub.
                else:
                    ppd.get_hash().update_item(package_id, value_index, package_status_options[0])

                package_id = ppd.get_hash().lookup_item(package_id)[1][0]

                # Padding the single digits with a leading space for prettier output.
                if int(package_id) < 10:
                    package_id = ' ' + package_id

                # Unpacking the hash table entry
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
                    f'| {status}'.ljust(23),
                    '|'
                )

        print('-' * 126)

        # Display truck status info if user chose to display info and status' for all packages at a specified time.
        if not single_package_lookup:

            # Calculate the first truck delivery duration if the truck has not yet returned to the hub.
            if truck_num == 1:
                first_truck_diff = wtime.time_difference(
                    self.first_truck_delivery_times[delivered_count - 1], FIRST_TRUCK_DEPARTURE_TIME
                )
                first_truck_diff = wtime.convert_int_seconds_to_string_time(first_truck_diff)

            # Calculate the second truck delivery duration if the truck has not yet returned to the hub.
            if truck_num == 2:
                second_truck_diff = wtime.time_difference(
                    self.second_truck_delivery_times[delivered_count - 1], self.second_truck_departure_time
                )
                second_truck_diff = wtime.convert_int_seconds_to_string_time(second_truck_diff)

            # Calculate the third truck delivery duration if the truck has not yet returned to the hub.
            if truck_num == 3:
                third_truck_diff = wtime.time_difference(
                    self.third_truck_delivery_times[delivered_count - 1], self.first_truck_delivery_times[-1]
                )
                third_truck_diff = wtime.convert_int_seconds_to_string_time(third_truck_diff)

            # Calculate the first truck delivery duration if the truck has returned to the hub.
            first_total_truck_diff = wtime.time_difference(
                self.first_truck_delivery_times[-1], FIRST_TRUCK_DEPARTURE_TIME
            )
            first_total_truck_diff = wtime.convert_int_seconds_to_string_time(first_total_truck_diff)

            # Calculate the second truck delivery duration if the truck has returned to the hub.
            second_total_truck_diff = wtime.time_difference(
                self.second_truck_delivery_times[-1], self.second_truck_departure_time
            )
            second_total_truck_diff = wtime.convert_int_seconds_to_string_time(second_total_truck_diff)

            # Calculate the third truck delivery duration if the truck has returned to the hub.
            third_total_truck_diff = wtime.time_difference(
                self.third_truck_delivery_times[-1], self.first_truck_delivery_times[-1]
            )
            third_total_truck_diff = wtime.convert_int_seconds_to_string_time(third_total_truck_diff)

            # If the truck has returned to the hub
            if truck_status == truck_status_options[2]:

                if truck_num == 1:
                    print('|', f'Truck {truck_num} Summary: {len(self.first_truck)} packages were delivered in '
                               f'{first_total_truck_diff} and traveled {round(sum(self.total_dist_first_truck), 2)} '
                               f'miles.'.center(122), '|')

                if truck_num == 2:
                    print('|', f'Truck {truck_num} Summary: {len(self.second_truck)} packages were delivered in '
                               f'{second_total_truck_diff} and traveled {round(sum(self.total_dist_second_truck), 2)} '
                               f'miles.'.center(122), '|')

                if truck_num == 3:
                    print('|', f'Truck {truck_num} Summary: {len(self.third_truck)} packages were delivered in '
                               f'{third_total_truck_diff} and traveled {round(sum(self.total_dist_third_truck), 2)} '
                               f'miles.'.center(122), '|')

            # If the truck is currently delivering packages.
            elif truck_status == truck_status_options[1]:

                if truck_num == 1:
                    if delivered_count == len(self.first_truck):
                        print('|', f'Truck {truck_num} has delivered all {delivered_count} packages in {first_truck_diff} and has'
                                   f' traveled {round(sum(self.total_dist_first_truck[:delivered_count]), 2)} miles and'
                                   f' is heading back to the hub.'.center(122), '|')
                    elif delivered_count == 0:
                        print('|', f'Truck {truck_num} has left the hub, but has not yet delivered any of the '
                                   f'{len(self.first_truck)} packages.'.center(122), '|')
                    else:
                        print('|', f'Truck {truck_num} has delivered {delivered_count}/{len(self.first_truck)} packages in '
                                   f'{first_truck_diff} and has traveled'
                                   f' {round(sum(self.total_dist_first_truck[:delivered_count]), 2)} miles.'
                                   f''.center(122), '|')

                if truck_num == 2:
                    if delivered_count == len(self.second_truck):
                        print('|', f'Truck {truck_num} has delivered all {delivered_count} packages in {second_truck_diff} and '
                                   f'has traveled {round(sum(self.total_dist_second_truck[:delivered_count]), 2)} miles'
                                   f' and is heading back to the hub.'.center(122), '|')
                    elif delivered_count == 0:
                        print('|', f'Truck {truck_num} has left the hub, but has not yet delivered any of the '
                                   f'{len(self.second_truck)} packages.'.center(122), '|')
                    else:
                        print('|', f'Truck {truck_num} has delivered {delivered_count}/{len(self.second_truck)} packages in '
                                   f'{second_truck_diff} and has traveled '
                                   f'{round(sum(self.total_dist_second_truck[:delivered_count]), 2)} miles.'
                                   f''.center(122), '|')

                if truck_num == 3:
                    if delivered_count == len(self.third_truck):
                        print('|', f'Truck {truck_num} has delivered all {delivered_count} packages in {third_truck_diff} and has'
                                   f' traveled {round(sum(self.total_dist_third_truck[:delivered_count]), 2)} miles and'
                                   f' is heading back to the hub.'.center(122), '|')
                    elif delivered_count == 0:
                        print('|', f'Truck {truck_num} has left the hub, but has not yet delivered any of the '
                                   f'{len(self.third_truck)} packages.'.center(122), '|')
                    else:
                        print('|', f'Truck {truck_num} has delivered {delivered_count}/{len(self.third_truck)} packages in '
                                   f'{third_truck_diff} and has traveled '
                                   f'{round(sum(self.total_dist_third_truck[:delivered_count]), 2)} miles.'
                                   f''.center(122), '|')

            # If the truck is still at the hub and has not started delivering packages yet.
            else:
                print('|', f'Truck {truck_num} has not left the hub yet.'.center(122), '|')

            print('-' * 126)

            # Calculate the total distance that all trucks traveled to deliver all the packages.
            self.total_distance_traveled = round(
                sum(self.total_dist_first_truck) +
                sum(self.total_dist_second_truck) +
                sum(self.total_dist_third_truck), 2
            )

            # Calculate the total distance that all trucks traveled to deliver all the packages without returning trucks
            # 2 and 3 to the hub.
            total_distance_without_returning_trucks_two_and_three_to_the_hub = round(
                sum(self.total_dist_first_truck) +
                sum(self.total_dist_second_truck[:-1]) +
                sum(self.total_dist_third_truck[:-1]), 2
            )

            # Calculate the total time it took for all the packages to be delivered.
            total_delivery_time_seconds = (
                    wtime.convert_string_time_to_int_seconds(first_total_truck_diff) +
                    wtime.convert_string_time_to_int_seconds(second_total_truck_diff) +
                    wtime.convert_string_time_to_int_seconds(third_total_truck_diff)
            )

            # Convert total delivery time from seconds to time format.
            self.total_delivery_time = wtime.convert_int_seconds_to_string_time(total_delivery_time_seconds)

            # Print output of the total distance traveled and the total time it took to deliver all packages.
            if truck_num == 3 and truck_status == truck_status_options[2]:
                print(f'\nTotal combined distance traveled: {self.total_distance_traveled} miles '
                      f'({total_distance_without_returning_trucks_two_and_three_to_the_hub} miles if trucks 2 and 3 '
                      'are left in the field, but that\'s not realistic)')
                print(f'Total time trucks were delivering packages(hub to hub): {self.total_delivery_time} (HH:MM:SS)')
