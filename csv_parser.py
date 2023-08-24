print('Hi from csv_parser.py')

import csv
from hash_table import HashTable

with open('./data/input_data.csv', newline='') as delivery_data:

    csv_data = csv.reader(delivery_data, delimiter=',')

    # row_count = sum(1 for row in csv_data)

    ht = HashTable()
    first_truck = []
    second_truck = []
    third_truck = []

    packages_to_be_delivered_together = set(())

    # Define dictionaries
    deliver = {}
    note = {}

    for package_details in list(csv_data):

        package_id = package_details[0]
        address = package_details[1]
        city = package_details[2]
        state = package_details[3]
        zipcode = package_details[4]
        deliver_by = package_details[5]
        package_weight = package_details[6]
        special_note = package_details[7]

        if 'Must be delivered with' in package_details[7]:
            package1 = int(package_details[7][-7:-5])
            packages_to_be_delivered_together.add(package1)
            package2 = int(package_details[7][-2:])
            packages_to_be_delivered_together.add(package2)

        if deliver_by != 'EOD':
            first_truck.append(package_details)

        # Dictionaries to count the occurrences of each thing
        if deliver_by not in deliver:
            deliver[deliver_by] = 1
        else:
            deliver[deliver_by] += 1

        if special_note not in note:
            note[special_note] = 1
        else:
            note[special_note] += 1

        ht.add_package(package_id, package_details)

    print(f'\nDeliver Time: {deliver.items()}')
    print(f'Special note: {note.items()}')
    print(f'Packages that need to be delivered together: {packages_to_be_delivered_together}')

    def get_hash():
        print('Hi from get_hash()')
        return ht
