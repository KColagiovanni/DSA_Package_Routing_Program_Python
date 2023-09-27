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

    @staticmethod
    def get_hash():
        return ht

    # Parse package data and send it to the hash table - [O(n)]
    @staticmethod
    def get_package_data():

        package_data_list = list(ParseCsvData.get_input_data())

        # Unpack the input data
        for package_details in package_data_list:

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

    # Match input_data.csv with distance_name_data.csv and return a dict with the important data - [O(n)]
    def sync_csv_data(self, package_data):

        name_data = self.get_distance_name_data()

        if package_data[1][1] in self.record.keys():
            self.record[package_data[1][1]]['Package ID'].update(
                {len(self.record[package_data[1][1]]['Package ID']) + 1: package_data[0]}
            )

        else:
            self.record.update({package_data[1][1]: {'Index': {}, 'Package ID': {1: package_data[0]}}})

        # For loop to iterate over the distance name data.
        for delivery_address in name_data:
            if package_data[1][1] == delivery_address[2]:
                self.record[package_data[1][1]]['Index'] = delivery_address[0]
