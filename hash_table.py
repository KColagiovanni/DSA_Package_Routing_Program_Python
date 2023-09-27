class HashTable:

    def __init__(self, table_size=40):

        self.hash_table = []
        self.table_size = table_size

        for bucket in range(self.table_size):
            self.hash_table.append([])

    def create_key(self, key):
        return int(key) % self.table_size

    def add_package(self, key, value):
        self.hash_table[self.create_key(key)] = [key, value]

    def lookup_item(self, key):
        return self.hash_table[self.create_key(key)]

    def update_item(self, key, value_index, new_value):
        self.hash_table[self.create_key(key)][1][value_index] = new_value
