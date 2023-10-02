from constant import *
import math
from bisect import bisect_right

class BPlusTreeNode:
    def __init__(self, parent=None, is_leaf=False):
        self.keys = []  # List of keys
        self.children = []  # List of indices to records/other TreeNodes
        self.is_leaf = is_leaf  # Flag to indicate whether it's a leaf node
        self.parent = parent # Pointer to parent node
        self.next = None
    
    # returns index of the child corresponding to the key we are searching for
    def index(self, key):
        # return bisect_right(self.keys, key)
        for i, item in enumerate(self.keys):
            if key < item:
                return i

        return len(self.keys)
        
    # splits a node up into two nodes once it is greater than size N
    # returns key to be put in parent node, and a list of the two split nodes
    def split(self):
        # ceiling division of len(self.keys) / 2
        mid = math.ceil(len(self.keys) / 2)

        right = BPlusTreeNode(self.parent, self.is_leaf)

        # split leaf node
        if self.is_leaf:
            right.keys, right.children = self.keys[mid:], self.children[mid:]
            self.keys, self.children = self.keys[:mid], self.children[:mid]

            # add right node as self's next pointer
            right.next = self.next
            self.next = right

            return right.keys[0], self, right
        
        # split internal node
        else:
            right.keys, right.children = self.keys[mid + 1:], self.children[mid + 1:]
            # assign new parent to existing children
            for child in right.children:
                child.parent = right

            # this key is to be returned for insertion into a parent node (parent of self and right)
            key = self.keys[mid]
            self.keys, self.children = self.keys[:mid], self.children[:mid + 1]

            return key, self, right



# Create a data structure for the B+ tree
class BPlusTree:
    def __init__(self):
        self.root = BPlusTreeNode(is_leaf=True)  # Initialize with a root leaf node

    def insert(self, key, value):
        # find the leaf node to insert in the key, value pair
        leaf_node = self.find(key)

        # if key is already in the leaf node, append the value [block_index, record_index_within_block]
        # to the children list
        if key in leaf_node.keys:
            # this is list.index NOT node.index
            index = leaf_node.keys.index(key)
            leaf_node.children[index].append(value)
            return      
        else:
            # position to insert new key in old node
            i = leaf_node.index(key)
            leaf_node.keys.insert(i, key)
            leaf_node.children.insert(i, [value])

        # if num keys > N (max keys per node)
        if len(leaf_node.keys) > N:
            insert_key, left_node, right_node = leaf_node.split()
            self.insert_index(insert_key, left_node, right_node)
    
    # update children's parent node to point to children
    def insert_index(self, key, left_child, right_child):
        parent = left_child.parent

        # create a new root if parent doesn't exist
        if not parent:
            self.root = BPlusTreeNode()
            # assign children to new root
            left_child.parent = self.root
            right_child.parent = self.root
            # new key (bound) for the two children
            self.root.keys = [key]
            # reference to children from the root
            self.root.children = [left_child, right_child]
            return
        
        # insert new key (index i) and right_child (index i+1) to parent node
        i = parent.index(key)
        parent.keys.insert(i, key)
        parent.children.insert(i+1, right_child)
        # parent[key] = children
        
        # recursively split and insert if num keys > N (max keys per node)
        if len(parent.keys) > N:
            insert_key, left_node, right_node = parent.split()
            self.insert_index(insert_key, left_node, right_node)

    # Returns the leaf node where the key should be at
    def find(self, key):
        node = self.root
        while not node.is_leaf:
            node = node.children[node.index(key)]
        return node
    
    def show(self, node=None, file=None, _prefix="", _last=True):
        """Prints the keys at each level."""
        # print('1', type(node))
        if node is None:
            node = self.root
        # print('2', type(node))
        
        # print('cur', node) 
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        # print('children', node.children)
        # print('parent', node.parent)
        # print('==================================================')
        _prefix += "   " if _last else "|  "

        if not node.is_leaf:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.children):
                _last = (i == len(node.children) - 1)
                self.show(child, file, _prefix, _last)
        # else:
        #     print('children', node.children)

    def search(self, key, key2=None):
        # Search for a key in the B+ tree and return associated values
        # Implement search algorithm``
        c_idx = 0 # Additional no. index nodes accessed on top of tree height
        result = [] # List of record pointers

        # Find pointers for all records where key = query key
        leaf_node = self.find(key)
        index = leaf_node.keys.index(key)
        result += leaf_node.children[index]

        # Range query
        if key2 is not None:
            found = False 

            while key <= key2:
                # Append results
                if found:
                    result += leaf_node.children[index]

                # Locate next key
                index += 1
                if index < len(leaf_node.keys): #Next key is in the same block
                    key = leaf_node.keys[index]
                    found = True
                elif leaf_node.next is not None:
                    leaf_node = leaf_node.next #Next key is in the neighbouring block
                    index = 0
                    key = leaf_node.keys[index]
                    found = True
                    c_idx += 1
                else: #Reach end of leaf nodes before upper bound of range query is hit
                    break
                

        return result, c_idx

    # def delete(self, key):
    #     # Delete the key in the B+ tree and the array that the last layer points to
        
    def delete(self, key, node=None):
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