import csv
from hash_table import HashTable

ht = HashTable()


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


def find_shortest_distance(distances):
    min_dist = distances[0]
    for distance in distances:
        if distance is not None and distance != '' and float(distance) > 0:
            if distance < min_dist:
                min_dist = distance
            # print(f'Distance list: {distance} miles')
    print(f'Shortest distance is: {min_dist} miles')
    print(f'Shortest distance index: {distances.index(str(min_dist))}')
    return distances.index(str(min_dist))


def match_distance_files_to_package_id():

    record = {}

    package_data = get_input_data()
    data = get_distance_data()
    name_data = get_distance_name_data()
    # print(f'\npackage_data({len(package_data)} records): {package_data}')
    # print(f'\ndata({len(data)} records): {data}')
    # print(f'\nname_data({len(name_data)} records): {name_data}')
    
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

    print(f'\ndict: {record}')
    return record


def calc_delivery_time(truck_list):
    # Trucks move at 18MPH    
    # for delivery in truck_list:
    pass


# Need to know total distance
# need to know where each package is at any given time

def load_trucks(package_id_data, distance_list):
    
    # First truck is loaded and leaves the hub at 8:00AM
    first_truck, second_truck, third_truck = [], [], []

    distance_data_index = find_shortest_distance(distance_list)
    print(f'Distance data index is: {distance_data_index}')
    print(f'distance_list is: {distance_list}')

    if len(first_truck) < 17:
        first_truck.append(distance_list)
    elif len(second_truck) < 17:
        second_truck.append(distance_list)
    elif len(third_truck) < 17:
        third_truck.append(distance_list)
    else:
        print('There was an error')
    # load_trucks(match_distance_files_to_package_id()[get_distance_name_data()])