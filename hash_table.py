class HashTable:
    """
    A hash table data structure that implements an associative list, a.k.a. a dictionary, which is an abstract data type
    that maps keys to values.

    Time Complexity: O(n) - Creating the empty list/array of size n.

    Attributes:
        hash_table(list): A list that will be used as a bucket.
        table_size(int): The size of the hash table.
    """
    def __init__(self, table_size=40):

        self.hash_table = []
        self.table_size = table_size

        # Create an empty list/array of size "table_size" that will be used to store bucket keys.
        for bucket in range(self.table_size):
            self.hash_table.append([])

    def create_key(self, key):
        """
        This method is a hash function used to compute an index, into a list of buckets.

        Time Complexity: O(1)

        Parameters:
            key(int): The value that is used as the bucket where the data will be stored.

        Return: None
        """
        return int(key) % self.table_size

    def add_package(self, key, value):
        """
        This method is used to add values to the hash table.

        Time Complexity: O(1)

        Parameters:
            key(int): The value that is used as the bucket where the data will be stored.
            value(list): The value to be stored in the bucket.

        Return: None
        """
        self.hash_table[self.create_key(key)] = [key, value]

    def lookup_item(self, key):
        """
        This method is used to look up/view an item that has been added to the hash table.

        Time Complexity: O(1)

        Parameters:
            key(int): The value that is used as the bucket where the data will be stored.

        Return(list): The value that is stored in the bucket.
        """
        return self.hash_table[self.create_key(key)]

    def update_item(self, key, value_index, new_value):
        """
        This method is used to update a value that has already been added to the hash table.

        Time Complexity: O(1)

        Parameters:
            key(int): The value that is used as the bucket where the data will be stored.
            value_index(int): The index of the stored list where the update will happen.
            new_value(any): The updated value.

        Return: None
        """
        self.hash_table[self.create_key(key)][1][value_index] = new_value
