import csv
import datetime
from hash_table import HashTable

ht = HashTable()
addresses = [0]
# num_of_packages = 0
distance_traveled = []
been_loaded = []
DELIVERY_TRUCK_SPEED_MPH = 18
MAX_PACKAGES_PER_TRUCK = 16
FIRST_TRUCK_DEPARTURE_TIME = '8:00:00'
# record = {}


class ParseCsvData:

    @staticmethod
    def get_input_data():
        with open('./data/input_data.csv', newline='') as delivery_data:

            package_data = csv.reader(delivery_data, delimiter=',')

            return list(package_data)

    @staticmethod
    def get_distance_data():
        with open('./data/distance_data.csv', newline='') as distance_data:

            distance_data = csv.reader(distance_data, delimiter=',')

            return list(distance_data)

    @staticmethod
    def get_distance_name_data():
        with open('./data/distance_name_data.csv', newline='') as distance_name_data:

            distance_name_data = csv.reader(distance_name_data, delimiter=',')

            return list(distance_name_data)


class Packages(ParseCsvData):

    def __init__(self):

        self.first_truck = []
        self.second_truck = []
        self.second_truck_departure_time = ''
        self.third_truck = []
        self.total_packages_loaded = 0
        self.high_priority_count = 0
        self.record = {}

    # Parse package data and send it to the hash table [O(n)]
    @staticmethod
    def get_package_data(package_list):

        desired_data = []
        special_note = ''
        delivery_status = ['At the hub', 'En route', 'Delivered']

        #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        # Define dictionaries
        deliver = {}
        note = {}
        addresses = {}
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        for package_details in list(package_list):

            package_id = package_details[0]
            address = package_details[1]
            city = package_details[2]
            state = package_details[3]
            zipcode = package_details[4]
            deliver_by = package_details[5]
            package_weight = package_details[6]
            special_note = package_details[7]

            desired_data = [package_id, address, deliver_by, city, zipcode, package_weight, delivery_status[0], special_note]

            ht.add_package(int(package_id), desired_data)  # O(1)

            print(f'{package_id} and {desired_data} have been added to the hash table')

        return len(package_list)

    # Analyze the special notes and deliver by times and add packages to trucks as needed [O(1)]
    def analyze_package_data(self, key):

        package_data = ht.lookup_item(key)  # O(1)

        print(f'package_data is: {package_data}')

        # minimum_hour = 25
        # minimum_minute = 60
        packages_to_be_delivered_together = set(())
        # first_delivery = []

        print(f'Special Note is: {package_data[1][7]}')

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
                print(f'DELAYED | HIGH PRIORITY: {package_data[0]} - ETA: {package_eta} (Deliver by: {package_data[1][2]})')
                self.second_truck.insert(self.high_priority_count, int(package_data[0]))
                self.high_priority_count += 0
                been_loaded.append(int(package_data[0]))
                self.total_packages_loaded += 1
                self.second_truck_departure_time = package_eta + ':00'
            else:
                print(f'DELAYED | {package_data[0]} - ETA: {package_eta} (Deliver by: {package_data[1][2]})')
                self.third_truck.append(int(package_data[0]))
                been_loaded.append(int(package_data[0]))
                self.total_packages_loaded += 1

        # Loading packages into the specific trucks that special instructions request.
        if 'Can only be on truck' in package_data[1][7]:
            if package_data[1][7][-1] == '1':
                if int(package_data[0]) not in self.first_truck:
                    self.first_truck.append(int(package_data[0]))
                    been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1
            elif package_data[1][7][-1] == '2':
                if int(package_data[0]) not in self.second_truck:
                    self.second_truck.append(int(package_data[0]))
                    been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1
            elif package_data[1][7][-1] == '3':
                if int(package_data[0]) not in self.third_truck:
                    self.third_truck.append(int(package_data[0]))
                    been_loaded.append(int(package_data[0]))
                    self.total_packages_loaded += 1

        print(f'From get_package_data(), self.first_truck is: {self.first_truck}')
        print(f'From get_package_data(), self.second_truck is: {self.second_truck}')
        print(f'From get_package_data(), self.third_truck is: {self.third_truck}')

    @staticmethod
    def get_hash():
        return ht

    # Returns the index of the shortest distance [O(n)]
    @staticmethod
    def find_shortest_distance(distances, start_row=1):

        search_data = {
            'min_horizontal_index': 0,
            'min_vertical_index': 0,
            'traversal_direction': 'horizontal',
            'min_dist': float(distances[start_row][1]),
            'min_dist_location': 'horizontal'
        }

        # print(f'\nstart_row is: {start_row}')

        for search_index in range(1, len(distances[start_row])):
            # print(f'\ndistances[{start_row}][{search_index}] is: {distances[start_row][search_index]}')
            # print(f'distances[{search_index}][{start_row}] is: {distances[search_index][start_row]}')
            if distances[start_row][search_index] == '0.0':
                search_data['traversal_direction'] = 'vertical'

            # print(f'search_index is: {search_index}')
            # print(f'addresses is: {addresses}')
            if search_index in addresses:
                continue
            # print(f'search_data is {search_data}')
            if search_data['traversal_direction'] == 'horizontal':
                if distances[start_row][search_index] != '':
                    if float(distances[start_row][search_index]) < search_data['min_dist']:
                        if float(distances[start_row][search_index]) != 0:
                            search_data['min_dist'] = float(distances[start_row][search_index])
                            search_data['min_dist_location'] = 'horizontal'
                            search_data['min_horizontal_index'] = search_index
                            # print(f'min_dist is: {search_data["min_dist"]}')

            if search_data['traversal_direction'] == 'vertical':
                if distances[search_index][start_row] != '':
                    if float(distances[search_index][start_row]) < search_data['min_dist']:
                        if float(distances[search_index][start_row]) != 0:
                            search_data['min_dist'] = float(distances[search_index][start_row])
                            search_data['min_dist_location'] = 'vertical'
                            search_data['min_vertical_index'] = search_index
                            # print(f'min_dist is: {search_data["min_dist"]}')

        # print(f'\nmin_dist: {search_data["min_dist"]} miles')
        distance_traveled.append(float(search_data["min_dist"]))
        # print(f'Distance traveled list: {distance_traveled}')
        # print(f'Total Distance Traveled: {round(sum(distance_traveled), 2)} miles')
        if start_row not in addresses:
            addresses.append(start_row)
        if search_data["min_horizontal_index"] == 0 and search_data["min_vertical_index"] == 0:
            for index in range(1, len(distances[start_row])):
                if index not in addresses:
                    search_data['min_horizontal_index'] = index
                    search_data['min_vertical_index'] = index

        if search_data['min_dist_location'] == 'horizontal':
            return search_data["min_horizontal_index"]
        if search_data['min_dist_location'] == 'vertical':
            return search_data['min_vertical_index']

    # Check if a truck can be loaded more efficiently if it was initially loaded with
    # required packages prior to beling loaded by the shortest distance method
    def maximize_efficiency(self, index):
        pass

    # Match input_data.csv with distance_name_data.csv and return a dict with the important data [O(n^2)]
    def sync_csv_data(self, package_data):

        # package_data = self.get_input_data()
        # data = self.get_distance_data()
        name_data = self.get_distance_name_data()

        # print(f'package_data is: {package_data}')
        # print(f'package_data[1][1] is: {package_data[1][1]}')
        # print(f'name_data is: {name_data}')

        if package_data[1][1] in name_data:
            print(f'\nname_data is: {name_data[2]}\n')

        if package_data[1][1] in self.record.keys():
            # print(f"len(self.record[package_data[1][1]]['Package ID']) is: {len(self.record[package_data[1][1]]['Package ID'])}")
            # self.record[package_data[1][1]]['Package ID'][2] = package_data[0]
            self.record[package_data[1][1]]['Package ID'].update({len(self.record[package_data[1][1]]['Package ID']) + 1: package_data[0]})

        # self.record.update({package_data[1][1]: {'Index': {}, 'Package ID': {len(self.record[package_data[1][1]]['Package ID']) + 1: package_data[0]}}})
        else:
            self.record.update({package_data[1][1]: {'Index': {}, 'Package ID': {1: package_data[0]}}})

            # self.record.update({package_data[1][1]: {'Index': {}, 'Package ID': {1: package_data[0]}}})

        for delivery_address in name_data:
            if package_data[1][1] == delivery_address[2]:
                self.record[package_data[1][1]]['Index'] = delivery_address[0]
        #     # print(f'delivery_address is: {delivery_address}')
        #     # print(f'package_data[0] is {package_data[0]}')
        #     # print(f'package_data[1] is: {package_data[1]}')
        #     if delivery_address[2] == package_data[1][1]:
        #         print(f'{delivery_address[2]} == {package_data[1][1]}')
        #         # print(f'\nmatch at index {delivery_address[0]}')
        #         # print(f'record[delivery_address[2]] is {record[delivery_address[2]]}')
        #         self.record.update({delivery_address[2]: {'Index': int(delivery_address[0]), 'Package ID': {}}})
        #         # num_of_packages = len(self.record[delivery_address[2]]['Package ID'])
        #         # print(f'num_of_packages is {num_of_packages}')
        #         print(f'self.record.get(delivery_address[2]) is: {delivery_address[2] in self.record}')
        #         print(f"len(self.record[delivery_address[2]]['Package ID']) is: {len(self.record[delivery_address[2]]['Package ID'])}")
        #         if not delivery_address[2] in self.record:
        #             print(f'if: package_data[0] is {package_data[0]}')
        #             print(f'if: record[delivery_address[2]] is {self.record[delivery_address[2]]}')
        #             # self.record.update({delivery_address[2]: {'Index': int(delivery_address[0]), 'Package ID': {1: int(package_data[0])}}})
        #             self.record[delivery_address[2]]['Package ID'].update({1: int(package_data[0])})
        #             # print(f"record[delivery_address[2]]['Package ID'][package_count] is {record[delivery_address[2]]['Package ID'][package_count]}")
        #             # print(f'package_data from sync_csv_data() is: {package_data}')
        #         else:
        #             print(f'else: package_data[0] is {package_data[0]}')
        #             print(f'else: record[delivery_address[2]] is {self.record[delivery_address[2]]}')
        #             # record[delivery_address[2]]['Package ID'][package_count] = package_data[0]
        #             self.record[delivery_address[2]]['Package ID'].update({len(self.record[delivery_address[2]]['Package ID']) + 1: int(package_data[0])})
        #             # self.record.update({delivery_address[2]: {'Index': int(delivery_address[0]), 'Package ID': {num_of_packages: int(package_data[0])}}})
        #             # print(f"record[delivery_address[2]]['Package ID'][package_count] is {record[delivery_address[2]]['Package ID'][package_count]}")
        #             # self.package_count += 1

        # for index in name_data:
        #     package_count = 1
        #     self.record.update({index[2]: {'Index': int(index[0]), 'Package ID': {}}})
        #
        #     for package_details in package_data:
        #         if package_details[1] == index[2]:
        #             if package_count == 1:
        #                 self.record[index[2]]['Package ID'][package_count] = (int(package_details[0]))
        #                 package_count += 1
        #             else:
        #                 self.record[index[2]]['Package ID'][package_count] = (int(package_details[0]))
        #                 package_count += 1

        # print(f'\nrecord is: {record}')
        return self.record

    # Calculate the delivery distance between each package in the pre-loaded list [O(n^3)]
    def calculate_truck_distance(self, package_list):

        truck_distance_list = []

        # Getting the next two lines is O(n^2) each
        hub_to_first_delivery = float(self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[package_list[0]][1]]["Index"]][0])
        last_delivery_to_hub = float(self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[package_list[-1] - 1][1]]["Index"]][0])
        # print(f'\nhub_to_first_delivery is: {hub_to_first_delivery} miles')
        # print(f'last_delivery_to_hub is: {last_delivery_to_hub} miles')

        truck_distance_list.append(hub_to_first_delivery)

        for distance in range(1, len(package_list)):
            # print(f'{self.first_truck[distance - 1]} is {self.get_distance_name_data()[self.first_truck[distance - 1]][2]}')

            # Getting the next two lines is O(n^2) each, and they're in a for loop, which makes it O(n^3)
            index1 = self.sync_csv_data()[self.get_input_data()[package_list[distance - 1] - 1][1]]["Index"]
            index2 = self.sync_csv_data()[self.get_input_data()[package_list[distance] - 1][1]]["Index"]

            # print(f'\ndistance is: {distance}')
            # print(f'first_truck[distance - 1] is: {package_list[distance - 1]}')  # & {package_list[distance]}')
            # print(f'get_input_data()[first_truck[distance - 1] - 1] is: {self.get_input_data()[package_list[distance - 1] - 1][1]}')
            # print(f'get_input_data()[first_truck[distance] - 1] is: {self.get_input_data()[package_list[distance] - 1][1]}')

            if index1 > index2:
                indexes = [index1, index2]
            else:
                indexes = [index2, index1]

            # print(f'get_distance_data()[{indexes[0]}][{indexes[1]}] is: {self.get_distance_data()[indexes[0]][indexes[1]]}')
            truck_distance_list.append(float(self.get_distance_data()[indexes[0]][indexes[1]]))

        truck_distance_list.append(float(last_delivery_to_hub))

        # print(f'\nself.first_truck_distance_list is: {truck_distance_list}')

        return round(sum(truck_distance_list), 2), truck_distance_list

    # Calculates the time it takes to go from one delivery to the next and also the total delivery time for the truck [O(n)]
    def calc_delivery_time(self, package_distance_list, departure_time):
        # Trucks move at 18MPH

        (hours, minutes, seconds) = departure_time.split(':')
        converted_departure_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

        cumulative_delivery_duration_list = []
        # individual_delivery_duration_list = []
        delivery_time_list = []
        total_duration = 0
        
        for package_distance in package_distance_list:
            duration = round((package_distance / DELIVERY_TRUCK_SPEED_MPH), 2)
            total_duration += duration    
            # individual_delivery_duration_list.append(duration)
            cumulative_delivery_duration_list.append(str(converted_departure_time + datetime.timedelta(hours=float(total_duration))))
            # print(f'\nfloat(duration) is: {float(duration)}')
            # print(f'delivery_time is: {converted_departure_time + datetime.timedelta(hours=float(duration))}')
            # print(f'cumlative_delivery_duration_list is: {converted_departure_time + datetime.timedelta(hours=float(total_duration))}')
            delivery_time_list.append(str(datetime.timedelta(hours=float(duration))))
        # print(f'Delivery Times: {delivery_time_list}')
        # print(f'Cumulative Delivery Times: {cumulative_delivery_duration_list}')
        return delivery_time_list, cumulative_delivery_duration_list

    # Loads packages onto the trucks, using recursion [O(n^3)]
    def load_trucks(self, package_id):

        package_id_data = self.get_input_data()[int(package_id) - 1]
        print(f'package_id_data is: {package_id_data}')
        print(f'\nself.get_hash().lookup_item(package_id)) is: {self.get_hash().lookup_item(package_id)}')

        distance_list = self.sync_csv_data(self.get_hash().lookup_item(package_id))[package_id_data[1]]  # [O(n)]

        # Load First Truck
        if len(self.first_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
            # print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1): # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.first_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.first_truck.append(distance_list.get('Package ID').get(package_num))
                        # print(f'{distance_list.get("Package ID").get(package_num)} has been appended to the first truck => {self.first_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Second Truck
        elif len(self.second_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
            # print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1): # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.second_truck:   
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.second_truck.append(distance_list.get('Package ID').get(package_num))
                        # print(f'Package {distance_list.get("Package ID").get(package_num)} has been appended to the second truck => {self.second_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Third Truck
        elif len(self.third_truck) + len(distance_list.get('Package ID')) <= MAX_PACKAGES_PER_TRUCK:
            # print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1): # [O(n)]
                if distance_list.get('Package ID').get(package_num) not in self.third_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.third_truck.append(distance_list.get('Package ID').get(package_num))
                        # print(f'{distance_list.get("Package ID").get(package_num)} has been appended to the third truck => {self.third_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        else:
            return

        if self.total_packages_loaded == len(self.get_input_data()):

            total_dist_first_truck = self.calculate_truck_distance(self.first_truck)  # [O(n^3)]
            total_dist_second_truck = self.calculate_truck_distance(self.second_truck)  # [O(n^3)]
            total_dist_third_truck = self.calculate_truck_distance(self.third_truck)  # [O(n^3)]

            print()
            print('#' * 120)
            print(' ' * 45 + 'All packages have been loaded')
            print('#' * 120)

            first_truck_delivery_times = self.calc_delivery_time(total_dist_first_truck[1], FIRST_TRUCK_DEPARTURE_TIME) # [O(n)]
            second_truck_delivery_times = self.calc_delivery_time(total_dist_second_truck[1], self.second_truck_departure_time) # [O(n)]
            third_truck_departure_times = self.calc_delivery_time(total_dist_third_truck[1], first_truck_delivery_times[1][-1]) # [O(n)]

            print(f'\nTruck 1 Package IDs: {self.first_truck}(# of packages: {len(self.first_truck)}, Distance: {total_dist_first_truck[0]} miles)')
            print(f'Truck 1 Distance List: {self.calculate_truck_distance(self.first_truck)[1]}(miles)')
            print(f'Truck 1 Delivery Times: {first_truck_delivery_times[1]}')
            print(f'Truck 1 Duration Times: {first_truck_delivery_times[0]}')

            print(f'\nTruck 2 Package IDs: {self.second_truck}(# of packages: {len(self.second_truck)}, Distance: {total_dist_second_truck[0]} miles)')
            print(f'Truck 2 Distance List: {self.calculate_truck_distance(self.second_truck)[1]}(miles)')
            print(f'Truck 2 Delivery Times: {second_truck_delivery_times[1]}')
            print(f'Truck 2 Duration Times: {second_truck_delivery_times[0]}')

            print(f'\nTruck 3 Package IDs: {self.third_truck}(# of packages: {len(self.third_truck)}, Distance: {total_dist_third_truck[0]} miles)')
            print(f'Truck 3 Distance List: {self.calculate_truck_distance(self.third_truck)[1]}(miles)')
            print(f'Truck 3 Delivery Times: {third_truck_departure_times[1]}')
            print(f'Truck 3 Duration Times: {third_truck_departure_times[0]}')

            print(f'\nTotal Distance traveled: {round(total_dist_first_truck[0] + total_dist_second_truck[0] + total_dist_third_truck[0], 2)} miles')
            print('#' * 120)

            # print('\n\n|><|><|><|><|><| Clearing Lists and Zeroing variables to be ready for another search |><|><|><|><|><|')
            distance_traveled.clear()
            addresses.clear()
            # print(f'distance_traveled is now : {distance_traveled}')
            addresses.append(0)
            # print(f'addresses is now: {addresses}')
            self.first_truck.clear()
            self.second_truck.clear()
            self.third_truck.clear()
            # print(f'first_truck is now: {self.first_truck}')
            # print(f'second_truck is now: {self.second_truck}')
            # print(f'third_truck is now: {self.third_truck}')
            self.total_packages_loaded = 0
            # print(f'self.total_packages_loaded is {self.total_packages_loaded}')
            been_loaded.clear()
            # print(f'been_loaded is now: {been_loaded}')
            return

        else:
            dist_list_index = distance_list.get("Index") # [O(n)]
            print(f'type(dist_list_index) is: {type(dist_list_index)}')
            shortest_dist = self.find_shortest_distance(self.get_distance_data(), dist_list_index) # [O(n^2)]
            dist_name = self.get_distance_name_data()[shortest_dist][2] # [O(n^2)]
            print(f'self.get_hash().lookup_item(package_id) is: {self.get_hash().lookup_item(package_id)}')
            print(f'self.sync_csv_data(self.get_hash().lookup_item(package_id)) is: {self.sync_csv_data(self.get_hash().lookup_item(package_id))}')
            print(f'self.sync_csv_data(self.get_hash().lookup_item(package_id))[dist_name] is: {self.sync_csv_data(self.get_hash().lookup_item(package_id))[dist_name]}')
            print(f'self.sync_csv_data(self.get_hash().lookup_item(package_id))[dist_name]["Package ID"] is: {self.sync_csv_data(self.get_hash().lookup_item(package_id))[dist_name]["Package ID"]}')
            self.load_trucks(self.sync_csv_data(self.get_hash().lookup_item(package_id))[dist_name]["Package ID"][1]) # [O(n^2)]
