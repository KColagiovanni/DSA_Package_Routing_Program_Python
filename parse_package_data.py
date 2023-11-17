import csv
from hash_table import HashTable
from wgups_time import WgupsTime

TABLE_SIZE = 40
SUBDIRECTORY = './data/'
DISTANCE_TABLE = 'WGUPS Distance Table.csv'
PACKAGE_FILE = 'WGUPS Package File.csv'

ht = HashTable(TABLE_SIZE)
wtime = WgupsTime()


class ParseCsvData:
    """
    Parse data from the provided CSV files and merge the data from the input and distance name files into a dictionary.

    Attributes: None
    """
    @staticmethod
    def get_input_data():
        """
        Parse the input data CSV file using the csv library and convert it into a list.

        Time Complexity: O(1)

        Parameters: None

        Returns:
            package_data(list): A list of the package input data in string format.
        """
        with open(SUBDIRECTORY + PACKAGE_FILE, newline='') as delivery_data:

            package_data = csv.reader(delivery_data, delimiter=',')

            return list(package_data)

    @staticmethod
    def get_distance_data():
        """
        Parse the distance table CSV file using the csv library and convert it into a list.

        Time Complexity: O(n)

        Parameters: None

        Returns:
            distance_data_list(list): A list of the distance data in string format.
        """
        with open(SUBDIRECTORY + DISTANCE_TABLE, newline='') as distance_table:

            distance_table = csv.reader(distance_table, delimiter=',')

            distance_data_list = [row[3:] for row in distance_table]

            return distance_data_list

    @staticmethod
    def get_distance_name_data():
        """
        Parse the distance table CSV file using the csv library and convert it into a list.

        Time Complexity: O(n)

        Parameters: None

        Returns:
            distance_name_data_list(list): A list of the distance name data in string format.
        """
        with open(SUBDIRECTORY + DISTANCE_TABLE, newline='') as distance_table:

            distance_table = csv.reader(distance_table, delimiter=',')

            distance_name_data_list = [row[:3] for row in distance_table]

            return distance_name_data_list


class Packages(ParseCsvData):
    """
    This class merges the needed data from the input_data.csv file and the distance_name_data.csv file with the data
    needed to load the trucks. This class inherits from the ParseCsvData class.

    Attributes:
        record(dict): This dictionary will hold specific package data for each deliver address.
        packages_to_be_delivered_together(set): This set it used to store the package id's of the packages that need to
        be delivered together.
    """

    def __init__(self):

        self.record = {}
        self.packages_to_be_delivered_together = set()

    @staticmethod
    def get_hash():
        """
        This method is used to access the hash table.

        Time Complexity: O(1)

        Parameters: None

        Returns:
            dict: The data that was returned from the hash table.
        """
        return ht

    @staticmethod
    def get_package_data():
        """
        This method takes the values from input_data.csv and adds them to a list with the name desired_data, then adds
        that list to the hash table using the package_id as the hash table key.

        Time Complexity: O(n)

        Parameters: None

        Returns:
            package_data_list(list): The unpacked values from the package file.
        """
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

            # Add data to the hash table
            ht.add_package(int(package_id), desired_data)  # O(1)

        return package_data_list

    def sync_csv_data(self, package_data):
        """
        This method combines data from the package data csv file and distance data csv files and adds that data to a
        nested python dictionary using the delivery address as a key for the main entry, and "Package ID(s)",
        "Deliver By", "Delayed ETA", "Truck", and "Deliver Together" as keys in the nested dictionary.

        Time Complexity: O(n)

        Parameters:
            package_data(list): A list with the data for each package that was provided in the ipackage data csv file.

        Returns:
            record(dict): A dictionary with package delivery data.
        """

        # Check if multiple packages are going to the same address. If so, append each one to the dictionary.
        if package_data[1][1] in self.record.keys():
            self.record[package_data[1][1]]['Package ID'].update({
                len(self.record[package_data[1][1]]['Package ID']) + 1: package_data[0]
            })

            # Append the highest priority (earliest) "Deliver By" data to each address delivery.
            if package_data[1][2] != 'EOD':
                if self.record[package_data[1][1]]['Deliver By'] != 'EOD':
                    if wtime.time_difference(self.record[package_data[1][1]]['Deliver By'], package_data[1][2]) > 0:
                        self.record[package_data[1][1]].update({'Deliver By': package_data[1][2]})
                else:
                    self.record[package_data[1][1]].update({'Deliver By': package_data[1][2]})

        # Add the first or only package and package data to the address that it will be delivered to.
        else:
            self.record.update({package_data[1][1]: {
                'Index': {},
                'Package ID': {1: package_data[0]},
                'Deliver By': package_data[1][2]}
            })

        # Adding packages to the dictionary that are delayed.
        if 'Delayed' in package_data[1][7]:
            if package_data[1][7][-8] == ' ':
                package_eta = package_data[1][7][-7:-3]
            else:
                package_eta = package_data[1][7][-8:-3]
            self.record[package_data[1][1]].update({'Delayed ETA': package_eta + ':00'})

        # Adding packages to the dictionary with truck number that the special instructions request.
        if 'Can only be on truck' in package_data[1][7]:

            # Truck 1
            if package_data[1][7][-1] == '1':
                self.record[package_data[1][1]].update({'Truck': 1})

            # Truck 2
            elif package_data[1][7][-1] == '2':
                self.record[package_data[1][1]].update({'Truck': 2})

            # Truck 3
            elif package_data[1][7][-1] == '3':
                self.record[package_data[1][1]].update({'Truck': 3})

        # Add packages to the dictionary that must be delivered together
        if 'Must be delivered with' in package_data[1][7]:
            self.packages_to_be_delivered_together.add(package_data[0])
            package1 = int(package_data[1][7][-7:-5])
            self.packages_to_be_delivered_together.add(package1)
            package2 = int(package_data[1][7][-2:])
            self.packages_to_be_delivered_together.add(package2)
            self.record[package_data[1][1]]['Deliver Together'] = self.packages_to_be_delivered_together

        name_data = self.get_distance_name_data()

        # For loop to iterate over the distance name data to add an index to each entry.
        for delivery_address in name_data:

            if package_data[1][1] == delivery_address[2]:
                self.record[package_data[1][1]]['Index'] = delivery_address[0]

        return self.record
