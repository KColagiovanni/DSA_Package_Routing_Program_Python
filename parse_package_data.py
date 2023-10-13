import csv
from hash_table import HashTable

ht = HashTable()


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

        self.record = {}
        self.packages_to_be_delivered_together = set()

    @staticmethod
    def get_hash():
        return ht

    # Parse package data and send it to the hash table - [O(n)]
    @staticmethod
    def get_package_data():

        package_data_list = list(ParseCsvData.get_input_data())

        # Unpack the input data
        for package_details in package_data_list:  # [O(n)]

            package_id = package_details[0]
            address = package_details[1]
            city = package_details[2]
            state = package_details[3]
            zipcode = package_details[4]
            deliver_by = package_details[5]
            package_weight = package_details[6]
            special_note = package_details[7]

            desired_data = [
                package_id,
                address,
                deliver_by,
                city,
                zipcode,
                package_weight,
                'At the Hub',  # Package Status
                special_note
            ]

            ht.add_package(int(package_id), desired_data)  # O(1)

        return package_data_list

    # Match input_data.csv with distance_name_data.csv and return a dict with the important data with the delivery
    # addresses as keys - [O(n)]
    def sync_csv_data(self, package_data):

        # Check if multiple packages are going to the same address. If so, append each one to the dictionary.
        if package_data[1][1] in self.record.keys():  # [O(n)]
            self.record[package_data[1][1]]['Package ID'].update({
                len(self.record[package_data[1][1]]['Package ID']) + 1: package_data[0]
            })

            # Append the highest priority "Deliver By" data to each address delivery.
            if package_data[1][2] != 'EOD':
                self.record[package_data[1][1]].update({'Deliver By': package_data[1][2]})

        # Add the first or only package and package data to the address that it will be delivered to.
        else:
            self.record.update({package_data[1][1]: {
                'Index': {},
                'Package ID': {1: package_data[0]},
                'Deliver By': package_data[1][2]}
            })

        # Adding packages to the dictionary that are delayed.
        if 'Delayed on flight' in package_data[1][7]:  # [O(n)]
            package_eta = package_data[1][7][-7:-3]

            self.record[package_data[1][1]].update({'Delayed ETA': package_eta + ':00'})

        # Adding packages to the dictionary with truck number that the special instructions request.
        if 'Can only be on truck' in package_data[1][7]:  # [O(n)]

            # For truck 1
            if package_data[1][7][-1] == '1':
                self.record[package_data[1][1]].update({'Truck': 1})

            # For truck 2
            elif package_data[1][7][-1] == '2':
                self.record[package_data[1][1]].update({'Truck': 2})

            # For truck 3
            elif package_data[1][7][-1] == '3':
                self.record[package_data[1][1]].update({'Truck': 3})

        # Adding packages to the dictionary that must be delivered together
        if 'Must be delivered with' in package_data[1][7]:  # [O(n)]
            self.packages_to_be_delivered_together.add(package_data[0])
            package1 = int(package_data[1][7][-7:-5])
            self.packages_to_be_delivered_together.add(package1)
            package2 = int(package_data[1][7][-2:])
            self.packages_to_be_delivered_together.add(package2)

            self.record[package_data[1][1]]['Deliver Together'] = self.packages_to_be_delivered_together

        name_data = self.get_distance_name_data()

        # For loop to iterate over the distance name data to add an index to each entry.
        for delivery_address in name_data:  # [O(n)]
            if package_data[1][1] == delivery_address[2]:
                self.record[package_data[1][1]]['Index'] = delivery_address[0]

        # print(f'\n{self.record}')
        return self.record