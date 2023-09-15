import csv
from hash_table import HashTable

ht = HashTable()
addresses = [0]
num_of_packages = 0
distance_traveled = []
been_loaded = []


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


# pcd = ParseCsvData()


class Packages(ParseCsvData):

    def __init__(self):

        self.first_truck = []
        self.first_truck_distance_list = []
        self.second_truck = []
        self.second_truck_distance_list = []
        self.third_truck = []
        self.third_truck_distance_list = []
        self.total_packages_loaded = 0
        self.max_packages_per_truck = 16

    def get_package_data(self, package_list):

        delivery_status = ['At the hub', 'En route', 'Delivered']
        min_hour = 25
        min_minute = 60
        packages_to_be_delivered_together = set(())
        first_delivery = []
        desired_data =[]

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

            desired_data = [package_id, address, deliver_by, city, zipcode, package_weight, delivery_status[0]]

            # ~~~~~~~~~~ Try using REGEX here ~~~~~~~~~~ #
            if 'Must be delivered with' in special_note:
                package1 = int(special_note[-7:-5])
                packages_to_be_delivered_together.add(package1)
                package2 = int(special_note[-2:])
                packages_to_be_delivered_together.add(package2)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            if 'Can only be on truck' in special_note:
                if special_note[-1] == '1':
                    self.first_truck.append(int(package_id))
                elif special_note[-1] == '2':
                    self.second_truck.append(int(package_id))
                elif special_note[-1] == '3':
                    self.third_truck.append(int(package_id))

            if deliver_by != 'EOD' and special_note == "None":
                hour = int(deliver_by[0:deliver_by.find(':')])
                minute = int(deliver_by[-5:-3])
                second = int(deliver_by[-2:])

                if hour < min_hour and minute < min_minute:
                    min_hour = hour
                    min_minute = minute
                    first_delivery = [deliver_by, package_id]

            if 'Delayed on flight' in special_note:
                package_eta = special_note[-7:]
                if deliver_by != 'EOD':
                    print(f'DELAYED | HIGH PRIORITY: {package_id} - ETA: {package_eta} (Deliver by: {deliver_by})')
                else:
                    print(f'DELAYED | {package_id} - ETA: {package_eta} (Deliver by: {deliver_by})')

            ht.add_package(package_id, desired_data)

        return desired_data, first_delivery

    @staticmethod
    def get_hash(self):
        return ht

    # Returns the index of the shortest distance
    def find_shortest_distance(self, distances, start_row=1):

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


    def sync_csv_data(self):

        record = {}

        package_data = self.get_input_data()
        data = self.get_distance_data()
        name_data = self.get_distance_name_data()

        for index in name_data:
            package_count = 1
            record.update({index[2]: {'Index': int(index[0]), 'Package ID': {}}})

            for package_details in package_data:
                if package_details[1] == index[2]:
                    if package_count == 1:
                        record[index[2]]['Package ID'][package_count] = (int(package_details[0]))
                        package_count += 1
                    else:
                        record[index[2]]['Package ID'][package_count] = (int(package_details[0]))
                        package_count += 1

        return record


    def calc_delivery_time(self, package_list):
        
        
        

        # Trucks move at 18MPH
        # for delivery in truck_list:
        pass

    # Need to calc min time in each delivery
    # Need to know total distance
    # need to know where each package is at any given time

    def load_trucks(self, package_id):

        package_id_data = self.get_input_data()[package_id - 1]
        distance_list = self.sync_csv_data()[package_id_data[1]]

        # Load First Truck
        if len(self.first_truck) + len(distance_list.get('Package ID')) <= self.max_packages_per_truck:
            print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.first_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.first_truck.append(distance_list.get('Package ID').get(package_num))
                        print(f'{distance_list.get("Package ID").get(package_num)} has been appended to the first truck => {self.first_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Second Truck
        elif len(self.second_truck) + len(distance_list.get('Package ID')) <= self.max_packages_per_truck:
            print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.second_truck:   
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.second_truck.append(distance_list.get('Package ID').get(package_num))
                        print(f'Package {distance_list.get("Package ID").get(package_num)} has been appended to the second truck => {self.second_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        # Load Third Truck
        elif len(self.third_truck) + len(distance_list.get('Package ID')) <= self.max_packages_per_truck:
            print(f'{distance_list.get("Package ID")} are together')
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.third_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.third_truck.append(distance_list.get('Package ID').get(package_num))
                        print(f'{distance_list.get("Package ID").get(package_num)} has been appended to the third truck => {self.third_truck}')
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1

        else:
            return

        if self.total_packages_loaded == len(self.get_input_data()):

            loaded_trucks = []
            loaded_trucks.append(self.first_truck)
            loaded_trucks.append(self.second_truck)
            loaded_trucks.append(self.third_truck)
            
            # print(f'\nself.get_distance_name_data() is: {self.get_distance_name_data()}')
            # print(f'\nself.sync_csv_data() is: {self.sync_csv_data()}')
            # print(f'\ndistance_list.get("Index") is: {distance_list.get("Index")}')
            # print(f'\ndistance_list is: {distance_list}')
            # print(f'\nself.get_input_data() is: {self.get_input_data()}')
            # print(f'\nself.sync_csv_data()[self.get_distance_name_data()[distance_list.get("Index")][2]] is: {self.sync_csv_data()[self.get_distance_name_data()[distance_list.get("Index")][2]]["Package ID"]}')
            # print(self.sync_csv_data()[self.get_distance_name_data()[self.find_shortest_distance(self.get_distance_data(), distance_list.get("Index"))][2]])

            # print(f'\nself.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[0]][1]]["Index"]][0] is: {self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[0]][1]]["Index"]][0]}')
            # print(f'\nself.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[-1]][1]]["Index"]][0] is: {self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[-1] - 1][1]]["Index"]][0]}')
            hub_to_first_delivery = float(self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[0]][1]]["Index"]][0])
            last_delivery_to_hub = float(self.get_distance_data()[self.sync_csv_data()[self.get_input_data()[self.first_truck[-1] - 1][1]]["Index"]][0])
            print(f'\nhub_to_first_delivery is: {hub_to_first_delivery} miles')
            print(f'last_delivery_to_hub is: {last_delivery_to_hub} miles')

            self.first_truck_distance_list.append(hub_to_first_delivery)

            for distance in range(1, len(self.first_truck)):
                # print(f'{self.first_truck[distance - 1]} is {self.get_distance_name_data()[self.first_truck[distance - 1]][2]}')
                index1 = self.sync_csv_data()[self.get_input_data()[self.first_truck[distance - 1] - 1][1]]["Index"]
                index2 = self.sync_csv_data()[self.get_input_data()[self.first_truck[distance] - 1][1]]["Index"]

                print(f'\ndistance is: {distance}')
                print(f'first_truck[distance - 1] is: {self.first_truck[distance - 1]}')# & {self.first_truck[distance]}')
                print(f'get_input_data()[first_truck[distance - 1] - 1] is: {self.get_input_data()[self.first_truck[distance - 1] - 1][1]}')
                print(f'get_input_data()[first_truck[distance] - 1] is: {self.get_input_data()[self.first_truck[distance] - 1][1]}')

                if index1 > index2:
                    indexes = [index1, index2]
                else:
                    indexes = [index2, index1]
                    
                print(f'get_distance_data()[{indexes[0]}][{indexes[1]}] is: {self.get_distance_data()[indexes[0]][indexes[1]]}')
                self.first_truck_distance_list.append(float(self.get_distance_data()[indexes[0]][indexes[1]]))

            self.first_truck_distance_list.append(float(last_delivery_to_hub))

            print(f'\nself.first_truck_distance_list is: {self.first_truck_distance_list}')            
            print()
            print('#' * 80)
            print(' ' * 25 + 'All packages have been loaded')
            print('#' * 80)
            print(f'Truck 1 Packages: {self.first_truck}(# of packages: {len(self.first_truck)}, Distance: {round(sum(self.first_truck_distance_list), 2)} miles)')
            print(f'Truck 2 Packages: {self.second_truck}(# of packages: {len(self.second_truck)}, Distance: {round(sum(self.second_truck_distance_list), 2)} miles)')
            print(f'Truck 3 Packages: {self.third_truck}(# of packages: {len(self.third_truck)}, Distance: {round(sum(self.third_truck_distance_list), 2)} miles)')
            print('#' * 80)

            print('\n\n|><|><|><|><|><| Clearing Lists and Zeroing variables to be ready for another search |><|><|><|><|><|')
            distance_traveled.clear()
            addresses.clear()
            print(f'distance_traveled is now : {distance_traveled}')
            addresses.append(0)
            print(f'addresses is now: {addresses}')
            self.first_truck.clear()
            self.first_truck_distance_list.clear()
            self.second_truck.clear()
            self.second_truck_distance_list.clear()
            self.third_truck.clear()
            self.third_truck_distance_list.clear()
            print(f'first_truck is now: {self.first_truck}')
            print(f'first_truck_distance_list is now: {self.first_truck_distance_list}')
            print(f'second_truck is now: {self.second_truck}')
            print(f'second_truck_distance_list is now: {self.second_truck_distance_list}')
            print(f'third_truck is now: {self.third_truck}')
            print(f'third_truck_distance_list is now: {self.third_truck_distance_list}')
            self.total_packages_loaded = 0
            print(f'self.total_packages_loaded is {self.total_packages_loaded}')
            been_loaded.clear()
            print(f'been_loaded is now: {been_loaded}')
            return

        else:
            dist_list_index = distance_list.get("Index")
            shortest_dist = self.find_shortest_distance(
                self.get_distance_data(), dist_list_index
            )
            dist_name = self.get_distance_name_data()[shortest_dist][2]
            self.load_trucks(self.sync_csv_data()[dist_name]["Package ID"][1])
