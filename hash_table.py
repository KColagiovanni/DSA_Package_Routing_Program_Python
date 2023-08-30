print('Hi from hash_table.py')

class HashTable:

    # def __init__(self, package_id_number, delivery_address, delivery_deadline, delivery_city, delivery_zip_code, package_weight, delivery_status, table_size=40):
    def __init__(self, table_size=40):

        self.hash_table = []
        self.table_size = table_size

        for bucket in range(self.table_size):
            self.hash_table.append([])

    def create_key(self, key):
        return int(key) % self.table_size

    def add_package(self, key, value):
        hash_key = self.create_key(key)
        entry = [key, value]
        self.hash_table[hash_key] = entry
        # print(f'hash_table: {self.hash_table}')

    def lookup_item(self, key):
        # print(f'lookup item key: {key}')
        hash_key = self.create_key(key)
        # print(f'self.hash_table[hash_key]: {self.hash_table[hash_key]}')
        # print(f'self.hash_table[hash_key][1][0]: {self.hash_table[hash_key][1][0]}')
        # for entry in self.hash_table[hash_key]:
            # print(f'entry[0] is {entry[0]}')
            # print(f'entry[1] is {entry[1]}')
            # return entry[1]
        # if self.hash_table[hash_key][1][0] == key:
        return self.hash_table[hash_key][1]
