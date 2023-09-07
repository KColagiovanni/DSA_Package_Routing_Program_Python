import csv
from hash_table import HashTable

ht = HashTable()

first_truck, second_truck, third_truck = [], [], []

def get_input_data():
    with open('./data/input_data.csv', newline='') as delivery_data:

        package_data = csv.reader(delivery_data, delimiter=',')

        return list(package_data)


def get_distance_data():
    with open('./data/distance_data.csv', newline='') as distance_data:

        distance_data = csv.reader(distance_data, delimiter=',')

        return list(distance_data)


def get_distance_name_data():
    with open('./data/distance_name_data.csv', newline='') as distance_name_data:

        distance_name_data = csv.reader(distance_name_data, delimiter=',')

        return list(distance_name_data)


def get_package_data(package_list):
        
    first_truck = []
    second_truck = []
    third_truck = []
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
                first_truck.append(int(package_id))
            elif special_note[-1] == '2':
                second_truck.append(int(package_id))
            elif special_note[-1] == '3':
                third_truck.append(int(package_id))

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


def get_hash():
    return ht


def find_shortest_distance(distances, start_row=2):
    # min_distance_index = []
    list_traversal_index = 0
    min_dist_count = 0
    # print(f'distances: {distances}')
    print(f'start row: {start_row}')
    # print(f'len(distances[start_row]) is: {len(distances[start_row])}')
    min_dist = float(distances[start_row][0])
    for col_index in range(0, len(distances[start_row]) - 1):
        print(f'\nmin_dist: {min_dist}(index: [{start_row}][{col_index}])')
        print(f'distances[{start_row}][{col_index}]: {distances[start_row][col_index]}')
        # print(f'distances[{start_row}][{col_index}] is: {distances[start_row][col_index]}')
        if distances[start_row][col_index] != '' and distances[start_row][col_index] is not None and float(distances[start_row][col_index]) > 0:
            # if float(distances[col_index] == 0):
                # for row_index in range(col_index)
            if float(distances[start_row][col_index]) < float(min_dist) and float(distances[start_row][col_index] != 0):
                # print(f'min_distance_index length is: {len(min_distance_index)}')
                min_dist = distances[start_row][col_index]
                min_dist_count += 1
            list_traversal_index += 1
                # if len(min_distance_index) > 0:
                #     min_distance_index.clear()
                # min_distance_index.append(start_row)
                # min_distance_index.append(col_index)
                # print(f'min distance_index is: {min_distance_index}')
                # print(f'min_distance_index length is: {len(min_distance_index)}')
        elif float(distances[start_row][col_index]) == 0:
            # print('distances == 0')
            for row in range(start_row, len(distances) - 1):
                # print(f'in for loop after distances == 0 (start_row is: {start_row} and col_indes is: {col_index} distances[start_row][col_index] is: {distances[start_row][col_index]})')
                # print(f'row is {row}')
                if float(distances[row][col_index]) != 0:
                    
                    # print(f'row is: {row}')
                    # print(f'col_index is: {col_index}')
                    print(f'\nmin_dist is: {min_dist}(index: [{row}][{col_index}])')
                    print(f'distances[{row}][{col_index}] is: {distances[row][col_index]}')
                    min_dist = distances[start_row][col_index]
                    min_dist_count += 1
                    # if len(min_distance_index) > 0:
                    #     min_distance_index.clear()
                    # min_distance_index.append(start_row)
                    # min_distance_index.append(col_index)
                list_traversal_index += 1
            break
        else:
            # print('Nan')
            continue
            # print(f'Distance list: {distance} miles')
    print(f'Shortest distance is: {min_dist} miles')
    # print(f'Shortest distance index: {distances[][]}')
    print(f'min_dist_count is: {min_dist_count}')
    print(f'list_traversal_index: {list_traversal_index}')
    print(f'returning {list_traversal_index} - {min_dist_count}')
    return list_traversal_index - min_dist_count


def sync_csv_data():

    record = {}

    package_data = get_input_data()
    data = get_distance_data()
    name_data = get_distance_name_data()

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


def calc_delivery_time(truck_list):
    # Trucks move at 18MPH    
    # for delivery in truck_list:
    pass

# Need to calc min time in each delivery
# Need to know total distance
# need to know where each package is at any given time

# def load_trucks(package_id):
def load_trucks(package_id):
    
    print(f'\npackage_id: {package_id}')
    print(f'type(package_id): {type(package_id)}')
    package_id_data = get_input_data()[package_id - 1]
    print(f'package_id_data is: {package_id_data}')
    # print(f'package_id_data[1] is: {package_id_data[1]}, package_id_data[0] is {package_id_data[0]}')

    distance_list = sync_csv_data()[package_id_data[1]]
    print(distance_list)
    # print(f'package_id_data is: {package_id_data}')
    # print(f'distance_list[Index]: {distance_list["Index"]}')
    # print(f'Distance List:Package ID(#{package_id_data[0]}) is: {distance_list.get("Package ID")}')
    # print(f'Distance List:Index(#{package_id_data[0]}) is: {distance_list.get("Index")}')
    # print(f'Shortest distance package_id_data: [{package_id_data[0]}][{find_shortest_distance(distance_list.get("Index"))}]')

    # print(f'distance_data(package_id_data {distance_list.get("Index")}) is: {get_distance_data()[distance_list.get("Index")]}')
    # print(f'Shortest distance[{distance_list.get("Index")}][{find_shortest_distance(get_distance_data()[distance_list.get("Index")])}]')
    # print(f'From {get_distance_name_data()[distance_list.get("Index")][2]} to {get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]}')
    sync_csv_data()
    # print(f'Index {ppd.find_shortest_distance(distance_list)} is {ppd.get_input_data()[ppd.find_shortest_distance(distance_list)][1]}')
    # ppd.load_trucks(ppd.match_distance_files_to_package_id[], distance_list)
    # print(f'Shortest distance is: {ppd.find_shortest_distance(distance_list)}')

    if len(first_truck) < 17:
        for package_num in range(1, len(distance_list.get('Package ID')) + 1):
            if distance_list.get('Package ID').get(package_num) not in first_truck:
                first_truck.append(distance_list.get('Package ID').get(package_num))
        print(f'Truck 1 Packages: {first_truck}')

    elif len(second_truck) < 17:
        for package_num in range(1, len(distance_list.get('Package ID')) + 1):
            if distance_list.get('Package ID').get(package_num) not in second_truck:
                second_truck.append(distance_list.get('Package ID').get(package_num))
        print(f'Truck 2 Packages: {second_truck}')

    elif len(third_truck) < 17:
        for package_num in range(1, len(distance_list.get('Package ID')) + 1):
            if distance_list.get('Package ID').get(package_num) not in third_truck:
                third_truck.append(distance_list.get('Package ID').get(package_num))
        print(f'Truck 3 Packages: {third_truck}')

    else:
        return

    # print(f'package ID: {sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]].get("Package ID")[1]}')
    # load_trucks(sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data()[distance_list.get("Index")])][2]].get("Package ID")[1])

    print(f'type(distance_list) is: {type(distance_list)}')
    y = find_shortest_distance(get_distance_data(), distance_list.get("Index"))
    print(f'\nget_distance_name_data()[2] is: {get_distance_name_data()[y][2]}')
    # print(f'find_shortest_distance(get_distance_data(), distance_list.get("Index") is: {[x, y]}')
    # print(f'Distance Name Data[{y}]: {get_distance_name_data()[y]}')
    # print(f'get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))] is: {get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))][2]}')
    print(f'sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))][2]] is: {sync_csv_data()[get_distance_name_data()[y][2]]["Package ID"][1]}')
    # load_trucks(sync_csv_data()[get_distance_name_data()[find_shortest_distance(get_distance_data(), distance_list.get("Index"))][2]]["Package ID"][1])
