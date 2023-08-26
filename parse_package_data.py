print('Hi from csv_parser.py')

import csv
from hash_table import HashTable
import os

with open('./data/input_data.csv', newline='') as delivery_data:

    package_data = csv.reader(delivery_data, delimiter=',')

    ht = HashTable()
    first_truck = []
    second_truck = []
    third_truck = []
    delivery_status = ['At the hub', 'En route', 'Delivered']

    packages_to_be_delivered_together = set(())

    #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
    # Define dictionaries
    deliver = {}
    note = {}
    addresses = {}
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    for package_details in list(package_data):

        package_id = package_details[0]
        address = package_details[1]
        city = package_details[2]
        state = package_details[3]
        zipcode = package_details[4]
        deliver_by = package_details[5]
        package_weight = package_details[6]
        special_note = package_details[7]

        desired_data = [package_id, address, deliver_by, city, zipcode, package_weight, delivery_status[0]]

        if 'Must be delivered with' in special_note:
            package1 = int(special_note[-7:-5])
            packages_to_be_delivered_together.add(package1)
            package2 = int(special_note[-2:])
            packages_to_be_delivered_together.add(package2)

        if 'Can only be on truck' in special_note:
            if special_note[-1] == '1' and len(first_truck) < 17:
                first_truck.append(int(package_id))        
            elif special_note[-1] == '2' and len(second_truck) < 17:
                second_truck.append(int(package_id))        
            elif special_note[-1] == '3' and len(third_truck) < 17:
                third_truck.append(int(package_id))   


        ht.add_package(package_id, desired_data)

        #~~~~~~~~~~~~~ TESTING PURPOSES ONLY. DELETE WHEN DONE ~~~~~~~~~~~~~#
        # Dictionaries to count the occurrences of each thing
        if deliver_by not in deliver:
            deliver[deliver_by] = 1
        else:
            deliver[deliver_by] += 1

        if special_note not in note:
            note[special_note] = 1
        else:
            note[special_note] += 1

        if address not in addresses:
            addresses[address] = 1
        else:
            addresses[address] += 1

    print(f'Packages on first truck: {len(first_truck)}')
    print(f'First truck: {first_truck}')
    print(f'Packages on second truck: {len(second_truck)}')
    print(f'Second truck: {second_truck}')
    print(f'Packages on third truck: {len(third_truck)}')
    print(f'Third truck: {third_truck}')

    print(f'\nDeliver Time: {deliver.items()}')
    print(f'Special note: {note.items()}')
    # print(f'Addresses: {addresses}')
    # print(f'Number of different addresses: {len(addresses)}')
    print(f'Packages that need to be delivered together: {packages_to_be_delivered_together}\n')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def get_hash():
        print('Hi from get_hash()')
        return ht
