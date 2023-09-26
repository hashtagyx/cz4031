from constant import *

# Define constants and configurations for the B+ tree
# BLOCK_SIZE = 400  # Block size in bytes
NODE_SIZE = BLOCK_SIZE  # Size of a B+ tree node is equal to block size

# Create a data structure for a B+ tree node
class BPlusTreeNode:
    def __init__(self, parent=None, is_leaf=False):
        self.keys = []  # List of keys
        self.children = []  # List of indices to records/other TreeNodes
        # todo: design of indices: must contain index of DatabaseFile.blocks, and index of record within each block
        self.is_leaf = is_leaf  # Flag to indicate whether it's a leaf node
        self.parent = parent
    
    # this defines the behavior of what happens when BPlusTreeNode[key] is called
    def __getitem__(self, key):
        return self.children[self.index(key)]
    
    # !!! for Leaf
    # def __setitem__(self, key, value):
    #     i = self.index(key)
    #     if key not in self.keys:
    #         self.keys[i:i] = [key]
    #         self.children[i:i] = [value]
    #     else:
    #         self.children[i - 1] = value
    
    # returns index of where the child (left) corresponding to the key is
    def index(self, key):
        for i, item in enumerate(self.keys):
            if key < item:
                return i
        return len(self.keys)
    # !!!
    def split(self):
        mid = len(self.keys) // 2
        # left = BPlusTreeNode(self.parent, self.is_leaf)
        right = BPlusTreeNode(self.parent, self.is_leaf)

        if self.is_leaf:
            # !!! splits
            # left.keys, left.children = self.keys[:mid], self.children[:mid]
            # self.keys, self.children = self.keys[mid:], self.children[mid:]

            # left.values.append(self) # to append the next pointer
            right.keys, right.children = self.keys[mid:], self.children[mid:]
            self.keys, self.children = self.keys[:mid], self.children[:mid]

            #
            if self.children[-1] is BPlusTreeNode:
                right.children.append(self.children[-1])
                self.children[-1] = right
            else:
                self.children.append(right)
            #

            # return self.keys[0], [left, self]
            return right.keys[0], [self, right]
        else:
            # left.keys, left.children = self.keys[:mid], self.children[:mid + 1]
            # for child in left.children:
            #     child.parent = left

            # key = self.keys[mid]
            # self.keys, self.children = self.keys[mid + 1:], self.children[mid + 1:]

            # return key, [left, self]
            right.keys, right.children = self.keys[mid + 1:], self.children[mid + 1:]
            for child in right.children:
                child.parent = right

            key = self.keys[mid]
            self.keys, self.children = self.keys[:mid], self.children[:mid + 1]

            return key, [self, right]

# Create a data structure for the B+ tree
class BPlusTree:
    def __init__(self):
        self.root = BPlusTreeNode(is_leaf=True)  # Initialize with a root leaf node

    def insert(self, key, value):
        # Insert a key-value pair into the B+ tree
        # Implement insertion algorithm

        # find the leaf node to insert in the key, value pair
        leaf_node = self.find(key)

        # if key is already in the leaf node, append the value (block_index, record_index_within_block)
        # to the children list
        if key in leaf_node.keys:
            index = leaf_node.keys.index(key)
            leaf_node.children[index].append(value)
        else:
            # !!!
            self.__setitem__(key, value, leaf_node)
    
    # this defines what happens when we call BPlusTree[i]
    def __setitem__(self, key, value, leaf_node=None):
        if not leaf_node:
            leaf_node = self.find(key)

        # !!! adds a list of length 1 with value (block_index, record_index_within_block)
        # leaf_node[key] = [value]
        if leaf_node.is_leaf:
            i = leaf_node.index(key)
            if key not in leaf_node.keys:
                leaf_node.keys[i:i] = [key]
                leaf_node.children[i:i] = [value]
            else:
                leaf_node.children[i - 1].append(value)
        else:
            i = leaf_node.index(key)
            leaf_node.keys[i:i] = [key]
            leaf_node.children.pop(i)
            leaf_node.children[i:i] = value

        if len(leaf_node.keys) > N:
            # !!!!
            self.insert_index(*leaf_node.split())
    
    def insert_index(self, key, children):
        # !!!
        parent = children[1].parent
        if not parent:
            self.root = BPlusTreeNode()
            children[0].parent = self.root
            children[1].parent = self.root
            self.root.keys = [key]
            self.root.children = children
            return
        
        # BPlusTreeNode's __setitem__ // Node's setitem
        i = parent.index(key)
        parent.keys[i:i] = [key]
        parent.children.pop(i)
        parent.children[i:i] = children # parent.children.insert(i, children)
        # parent[key] = children
        
        if len(parent.keys) > N:
            self.insert_index(*parent.split())

    # Returns the leaf node where the key should be at
    def find(self, key):
        node = self.root

        while not node.is_leaf:
            # !!!
            node = node[key]
        return node
    
    def show(self, node=None, file=None, _prefix="", _last=True):
        """Prints the keys at each level."""
        # print('1', type(node))
        if node is None:
            node = self.root
        # print('2', type(node))
        print('cur', node)
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        print('children', node.children)
        _prefix += "   " if _last else "|  "

        if not node.is_leaf:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.children):
                _last = (i == len(node.children) - 1)
                self.show(child, file, _prefix, _last)

    def search(self, key):
        # Search for a key in the B+ tree and return associated values
        # Implement search algorithm
        pass

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
