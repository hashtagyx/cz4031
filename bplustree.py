from constant import *

# Define constants and configurations for the B+ tree
# BLOCK_SIZE = 400  # Block size in bytes
NODE_SIZE = BLOCK_SIZE  # Size of a B+ tree node is equal to block size


# Create a data structure for a B+ tree node
class BPlusTreeNode:
    def __init__(self, pid, is_leaf=True):
        self.keys = []  # List of keys
        self.children = []  # List of indices to records/other TreeNodes
        self.parent = pid #index of DatabaseFile.blocks parent is stored 
        self.is_leaf = is_leaf  # Flag to indicate whether it's a leaf node

# Create a data structure for the B+ tree
class BPlusTree:
    def __init__(self, database):
        self.root = BPlusTreeNode(is_leaf=True)  # Initialize with a root leaf node
        self.database = database #reference to DatabaseFile instance

    def insert(self, key, value):
        # Insert a key-value pair into the B+ tree
        # Implement insertion algorithm
        # design of indices: non leaf nodes - store DatabaseFile.block ids of its children nodes  
        # leaf nodes - store (block_id, record_id) of records 
        pass

    def search(self, key):
        # Search for a key in the B+ tree and return associated values
        node = self.root
        found = False
        result = []

        while node.is_leaf == False:
            for i in range(N):
                if node.keys[i] > key:
                    loc = self.children[i] #(block id)
                    node = self.database.blocks[loc]
                    found=True
                    break
            if not found:
                loc = self.children[N]
                node = self.database.blocks[loc]
            found=False
        #at the leaf node
        for i in range(N):
            if node.keys[i]==key:
                for b_id, r_id in self.children[i]: #(block id, record id)
                    record = self.database.blocks[b_id][r_id]
                    result.append(record.serialize())
                break

        return result

    def delete(self, key):
        # Delete the key in the B+ tree and the array that the last layer points to
        pass

# # Initialize the B+ tree
# bplus_tree = BPlusTree()

# # Sample usage
# key = ...  # Key to insert
# value = ...  # Value associated with the key
# bplus_tree.insert(key, value)

# # Searching for a key
# search_key = ...  # Key to search for
# result = bplus_tree.search(search_key)
