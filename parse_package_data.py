import csv
from hash_table import HashTable

ht = HashTable()
addresses = [0]
num_of_packages = 0
distance_traveled = []

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
        self.second_truck = []
        self.third_truck = []
        self.total_packages_loaded = 0

    def get_package_data(self, package_list):

        # self.first_truck = []
        # self.second_truck = []
        # self.third_truck = []
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
                    # first_truck.append(int(package_id))

            if 'Delayed on flight' in special_note:
                package_eta = special_note[-7:]
                if deliver_by != 'EOD':
                    print(f'DELAYED | HIGH PRIORITY: {package_id} - ETA: {package_eta} (Deliver by: {deliver_by})')
                    # second_truck.append(int(package_id))
                else:
                    print(f'DELAYED | {package_id} - ETA: {package_eta} (Deliver by: {deliver_by})')
                    # third_truck.append(int(package_id))

            # if len(packages_to_be_delivered_together) > 0:
            #     if len(set(packages_to_be_delivered_together).intersection(set(first_truck))) / len(packages_to_be_delivered_together) > 0.5:
            #         first_truck.extend(set(packages_to_be_delivered_together).difference(set(first_truck)))

            ht.add_package(package_id, desired_data)

        return desired_data, first_delivery

    @staticmethod
    def get_hash(self):
        return ht

    # Returns the index of the shortest distance
    def find_shortest_distance(self, distances, start_row=1):
        ####################################### Original Version #######################################
        # min_dist = distances[start_row][1]
        # min_dist_index = 0
        # for col_index in range(1, len(distances[start_row])):
        #     # print(f'distances[{start_row}][{col_index}] is: {distances[start_row][col_index]}')
        #     if float(distances[start_row][col_index]) != 0:
        #         if float(distances[start_row][col_index]) < float(min_dist):
        #             min_dist = distances[start_row][col_index]
        #     else:
        #         break
        # # print(f'Distance list: {distance} miles')
        # # print(f'Shortest distance is: {min_dist} miles')
        # # print(f'Shortest distance index: {distances.index(str(min_dist))}')
        # print(f'min_dist: {min_dist} miles')
        # print(f'min_dist_index is: {min_dist_index}')
        # min_index = distances[start_row].index(min_dist)
        # return min_index

        ####################################### New Version #############################################
        # horizontal_index = 0
        # vertical_index = 0

        # if float(distances[start_row][0]) != 0:
        #     min_dist = float(distances[start_row][0])
        # else:
        #     min_dist = float(distances[start_row + 1][0])

        search_data = {
            'min_horizontal_index': 0,
            'min_vertical_index': 0,
            'traversal_direction': 'horizontal',
            'min_dist': float(distances[start_row][1]),
            'min_dist_location': 'horizontal'
        }

        for search_index in range(1, len(distances[start_row])):
            # print(f'\ndistances[start_row:{start_row}][search_index:{search_index}] is: {distances[start_row][search_index]}')
            # print(f'distances[search_index:{search_index}][start_row:{start_row}] is: {distances[search_index][start_row]}')
            if distances[start_row][search_index] == '0.0':
                search_data['traversal_direction'] = 'vertical'

            if search_index in addresses:
                continue
            if search_data['traversal_direction'] == 'horizontal':
                if distances[start_row][search_index] != '':
                    if float(distances[start_row][search_index]) < search_data['min_dist']:
                        if float(distances[start_row][search_index]) != 0:
                            search_data['min_dist'] = float(distances[start_row][search_index])
                            search_data['min_dist_location'] = 'horizontal'
                            search_data['min_horizontal_index'] = search_index
            if search_data['traversal_direction'] == 'vertical':
                if distances[search_index][start_row] != '':
                    if float(distances[search_index][start_row]) < search_data['min_dist']:
                        if float(distances[search_index][start_row]) != 0:
                            search_data['min_dist'] = float(distances[search_index][start_row])
                            search_data['min_dist_location'] = 'vertical'
                            search_data['min_vertical_index'] = search_index
            # print(f'search_data is: {search_data}')
        print(f'\nmin_dist: {search_data["min_dist"]} miles')
        distance_traveled.append(search_data["min_dist"])
        # distance_traveled += search_data['min_dist']
        print(distance_traveled)
        print(sum(distance_traveled))
        if start_row not in addresses:
            addresses.append(start_row)
        # print(f'addresses is: {addresses.sort()}')
        if search_data["min_horizontal_index"] == 0 and search_data["min_vertical_index"] == 0:
            for index in range(1, len(distances[start_row])):
                if index not in addresses:
                    
            # if search_data['min_dist_location'] == 'horizontal':
                    search_data['min_horizontal_index'] = index
            # if search_data['min_dist_location'] == 'vertical':
                    search_data['min_vertical_index'] = index

        if search_data['min_dist_location'] == 'horizontal':
            # print(f'returning {search_data["min_horizontal_index"]} from find_shortest_distance()\n')
            return search_data["min_horizontal_index"]
        if search_data['min_dist_location'] == 'vertical':
            # print(f'returning {search_data["min_vertical_index"]} from find_shortest_distance()\n')
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

    # print(f'\ndict: {record}')
        return record


    def calc_delivery_time(self, distance):

        # Trucks move at 18MPH
        # for delivery in truck_list:
        pass

    # Need to calc min time in each delivery
    # Need to know total distance
    # need to know where each package is at any given time

    # def load_trucks(package_id):
    def load_trucks(self, package_id):
        # print(f'\npackage_id added to load_trucks() is: {package_id}')
        package_id_data = self.get_input_data()[package_id - 1]
        distance_list = self.sync_csv_data()[package_id_data[1]]
        been_loaded = []
        # print(f'\npackage_id: {package_id}')
        # print(f'type(package_id): {type(package_id)}')
        # print(f'package_id_data is: {package_id_data}')
        # print(f'package_id_data[1] is: {package_id_data[1]}, package_id_data[0] is {package_id_data[0]}')

        # print(f'distance list: {distance_list}')
        # print(f'package_id_data is: {package_id_data}')
        # print(f'distance_list[Index]: {distance_list["Index"]}')
        # print(f'Distance List:Package ID(#{package_id_data[0]}) is: {distance_list.get("Package ID")}')
        # print(f'Distance List:Index(#{package_id_data[0]}) is: {distance_list.get("Index")}')
        # print(f'Shortest distance package_id_data: [{package_id_data[0]}][{find_shortest_distance(distance_list.get("Index"))}]')

        # print(f'distance_data(package_id_data {distance_list.get("Index")}) is: {get_distance_data()[distance_list.get("Index")]}')
        # print(f'Shortest distance[{distance_list.get("Index")}][{find_shortest_distance(get_distance_data()[distance_list.get("Index")])}]')
        # print(f'From {get_distance_name_data()[distance_list.get("Index")][2]} to {get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]}')
        # self.sync_csv_data() #~~~~~ Is this call necessary? ~~~~~
        # print(f'Index {ppd.find_shortest_distance(distance_list)} is {ppd.get_input_data()[ppd.find_shortest_distance(distance_list)][1]}')
        # ppd.load_trucks(ppd.match_distance_files_to_package_id[], distance_list)
        # print(f'Shortest distance is: {ppd.find_shortest_distance(distance_list)}')

        if len(self.first_truck) + len(distance_list.get('Package ID')) < 16:
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.first_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        # print(f'adding package id: {distance_list.get("Package ID")[package_num]} to truck 1')
                        self.first_truck.append(distance_list.get('Package ID').get(package_num))
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                #     else:
                #         print(f'Package ID: {distance_list.get("Package ID").get(package_num)} has already been loaded')
                # else:
                #     print(f'Package ID: {distance_list.get("Package ID").get(package_num)} is already on the first truck')

        elif len(self.second_truck) + len(distance_list.get('Package ID')) < 16:
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.second_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.second_truck.append(distance_list.get('Package ID').get(package_num))
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                #     else:
                #         print(f'Package ID: {distance_list.get("Package ID").get(package_num)} has already been loaded')
                # else:
                #     print(f'Package ID: {distance_list.get("Package ID").get(package_num)} is already on the second truck')

        elif len(self.third_truck) + len(distance_list.get('Package ID')) < 16:
            for package_num in range(1, len(distance_list.get('Package ID')) + 1):
                if distance_list.get('Package ID').get(package_num) not in self.third_truck:
                    if distance_list.get('Package ID').get(package_num) not in been_loaded:
                        self.third_truck.append(distance_list.get('Package ID').get(package_num))
                        been_loaded.append(distance_list.get('Package ID').get(package_num))
                        self.total_packages_loaded += 1
                #     else:
                #         print(f'Package ID: {distance_list.get("Package ID").get(package_num)} has already been loaded')
                # else:
                #     print(f'Package ID: {distance_list.get("Package ID").get(package_num)} is already on the third truck')

        else:
            return

        # print(f'number of packages: {len(self.get_input_data())}')
        # print(f'total_packages_loaded is: {self.total_packages_loaded}')
        if self.total_packages_loaded == len(self.get_input_data()):
            print()
            print('#' * 30)
            print('All packages have been loaded')
            print('#' * 30)
            return
        
        # print(been_loaded)
        # print(f'package ID: {sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]].get("Package ID")[1]}')
        # load_trucks(sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]].get("Package ID")[1])

        # print(f'type(distance_list) is: {type(distance_list)}')
        # y = find_shortest_distance(get_distance_data(), distance_list.get("Index"))
        # print(f'\nget_distance_name_data()[2] is: {get_distance_name_data()[y][2]}')
        # print(f'find_shortest_distance(get_distance_data(), distance_list.get("Index") is: {[x, y]}')
        # print(f'Distance Name Data[{y}]: {get_distance_name_data()[y]}')
        # print(f'get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))] is: {get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))][2]}')
        # print(f'distance_list.get("Package ID") is: {distance_list.get("Package ID")[1]}')
        print(f'Truck 1 Packages: {self.first_truck}')
        print(f'Truck 2 Packages: {self.second_truck}')
        print(f'Truck 3 Packages: {self.third_truck}')
        # num_of_packages = len(self.sync_csv_data()[self.get_distance_name_data()[self.find_shortest_distance(self.get_distance_data(), distance_list.get("Index"))][2]]["Package ID"])
        # print(f'Number of Packages: {num_of_packages}')
        # print(f'sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))][2]]["Package ID"][1] is: {self.sync_csv_data()[self.get_distance_name_data()[self.find_shortest_distance(self.get_distance_data(), distance_list.get("Index"))][2]]["Package ID"]}')
        self.load_trucks(self.sync_csv_data()[self.get_distance_name_data()[self.find_shortest_distance(self.get_distance_data(), distance_list.get("Index"))][2]]["Package ID"][1])
