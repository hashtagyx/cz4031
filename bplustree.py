from constant import *
import math
from bisect import bisect_right

# Define constants and configurations for the B+ tree
# BLOCK_SIZE = 400  # Block size in bytes
NODE_SIZE = BLOCK_SIZE  # Size of a B+ tree node is equal to block size

# Create a data structure for a B+ tree node
class BPlusTreeNode:
    def __init__(self, parent=None, is_leaf=False):
        self.keys = []  # List of keys
        self.children = []  # List of indices to records/other TreeNodes
        self.is_leaf = is_leaf  # Flag to indicate whether it's a leaf node
        self.parent = parent # Pointer to parent node
    
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
            self.children.append(right)

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
    
    def fusion(self, min_key):
        # this leaf node definitely has a parent (i.e. not a leaf node that is the root node)
        print('node.keys in fusion:', self.keys)
        # print('node is leaf: ', self.is_leaf)
        if self.is_leaf:
            print('----------------------------')
            print(isinstance(self.children[-1], BPlusTreeNode))
            if isinstance(self.children[-1], BPlusTreeNode):
                print(self.children[-1].parent == self.parent)
                print(self.children[-1].parent, self.parent)
                print(self.children[-1].keys, self.parent.keys)
                print(self.children[-1].keys)
            print('----------------------------')
            
            if isinstance(self.children[-1], BPlusTreeNode) and self.children[-1].parent == self.parent:
                next_node = self.children[-1]
                # print('curr node', self)
                # print('curr node children', self.children)
                # print('next_node', next_node)
                # print('next_node children', next_node.children)
                # print('next_node keys', next_node.keys)
                next_node.keys[0:0] = self.keys

                # print('next_node keys after insert', next_node.keys)
                # print(next_node.keys)
                # remove the pointer in left child before concatenating to the front of child node (left child join to the RIGHT CHILD)
                next_node.children[0:0] = self.children[:-1]
                print('next_node children', next_node.children)
                
                index = self.parent.index(self.keys[0])
                # index = self.parent.index(min_key)

                # make the prev node point to the fused node on the right (if there exists a prev node)
                if index >= 1:
                    print('Here')
                    prev_node = self.parent.children[index - 1]
                    prev_node.children[-1] = next_node

                print('new right leaf' , next_node.keys)
            # if self.next is not None and self.next.parent == self.parent:
                # self.next.keys[0:0] = self.keys
                # self.next.children[0:0] = self.children
            # there are no neighbouring nodes on the right i.e. fuse left
            else:
                # index = self.parent.index(self.keys[0])
                prev = self.parent.children[-2]
                
                prev.keys += self.keys
                prev.children = prev.children[:-1]
                prev.children += self.children

                print('new left leaf' , prev.keys)
            
                # self.prev.keys += self.keys
                # self.prev.children += self.children
                
        # if internal node/root node
        else:
            print('else in fusion', self.keys)
            # index = self.parent.index(self.keys[0])
            index = self.parent.index(min_key)
            # merge this node with the next node
            if index < len(self.parent.keys):
                # merge with the node on the right
                next_node = self.parent.children[index + 1]
                next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
                for child in self.children:
                    child.parent = next_node
                next_node.children[0:0] = self.children
            else:  # If self is the last node, merge with prev
                prev = self.parent.children[-2]
                prev.keys += [self.parent.keys[-1]] + self.keys
                for child in self.children:
                    child.parent = prev
                prev.children += self.children

    def borrow_key(self, minimum, min_key):
        # if len(self.keys) == 0:
        #     return False
        # index = self.parent.index(self.keys[0])
        index = self.parent.index(min_key)
        if self.is_leaf:
            if index < len(self.parent.keys) and len(self.children[-1].keys) > minimum:
                next_node = self.children[-1]
                self.keys += [next_node.keys.pop(0)]
                # self.children += [next_node.children.pop(0)]
                # self.children = self.children[:-1] + [next_node.children.pop(0)] + [self.children[-1]]
                self.children.insert(-2, next_node.children.pop(0))
                self.parent.keys[index] = next_node.keys[0]
                return True
            elif index != 0 and len(self.parent.children[index - 1].keys) > minimum:
                # if index >= 1:
                #     prev_node = self.parent.children[index - 1]
                prev_node = self.parent.children[index - 1]
                self.keys[0:0] = [prev_node.keys.pop()]
                self.children[0:0] = [prev_node.children.pop(-2)]
                # self.keys[0] is now prev_node.keys.pop()
                self.parent.keys[index - 1] = self.keys[0]
                return True

            return False
        else:
            if index < len(self.parent.keys):
                next_node = self.parent.children[index + 1]
                if len(next_node.keys) > minimum:
                    self.keys += [self.parent.keys[index]]

                    borrow_node = next_node.children.pop(0)
                    borrow_node.parent = self
                    self.children += [borrow_node]
                    self.parent.keys[index] = next_node.keys.pop(0)
                    return True
            elif index != 0:
                prev = self.parent.children[index - 1]
                if len(prev.keys) > minimum:
                    self.keys[0:0] = [self.parent.keys[index - 1]]

                    borrow_node = prev.children.pop()
                    borrow_node.parent = self
                    self.children[0:0] = [borrow_node]
                    self.parent.keys[index - 1] = prev.keys.pop()
                    return True

            return False

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
        
        print('cur', node) 
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        print('children', node.children)
        print('parent', node.parent)
        print('==================================================')
        _prefix += "   " if _last else "|  "

        if not node.is_leaf:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.children):
                _last = (i == len(node.children) - 1)
                self.show(child, file, _prefix, _last)
        # else:
        #     print('children', node.children)

    def search(self, key):
        # Search for a key in the B+ tree and return associated values
        # Implement search algorithm``
        pass

    # def delete(self, key):
    #     # Delete the key in the B+ tree and the array that the last layer points to
        
    def delete(self, key, node=None):
        if node is None:
            node = self.find(key)
        min_key = node.keys[0]
        # del node[key]
        print("before del node.keys, node.children, key:", node.keys, node.children, key)
        i = node.keys.index(key)
        # change to list delete

        # deleting the leaf node clearing the pointer
        del node.keys[i]
        del node.children[i]

        print("after del node.keys, node.children, key:", node.keys, node.children, key)

        # perform fusion 
        if len(node.keys) < MIN_LEAF:
            # special case leaf node is at the root level
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.children) > 0:
                    self.root = self.root.children[0]
                    self.root.parent = None
                return

            # borrow key from neighbours
            elif not node.borrow_key(MIN_LEAF, min_key):
                print(f"CANT BORROW FOR {key}")
                node.fusion(min_key)
                # fused_node = node.fusion(min_key)
                # remove internal node with key
                self.delete_internal_node(key, node.parent)
                # self.delete_internal_node(key, node.parent, fused_node)
                
    def delete_internal_node(self, key, node):
        # del node[key] for Node
        print("DELETING INTERNAL NODE")
        min_key = node.keys[0]
        i = node.index(key)
        del node.children[i]
        print('i', i, 'len of node keys', len(node.keys))
        if i < len(node.keys):
            del node.keys[i]
        else:
            del node.keys[i - 1]
        
        if len(node.keys) < MIN_INTERNAL:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.children) > 0:
                    self.root = self.root.children[0]
                    self.root.parent = None
                    # insert fused_node into self.root.keys and self.root.children
                    # change fused_node's parent
                return

            elif not node.borrow_key(MIN_INTERNAL, min_key):
                node.fusion(min_key)
                self.delete_internal_node(key, node.parent)
                # self.delete_internal_node(key, node.parent, fused_node)

# # Initialize the B+ tree
# bplus_tree = BPlusTree()

# # Sample usage
# key = ...  # Key to insert
# value = ...  # Value associated with the key
# bplus_tree.insert(key, value)

# # Searching for a key
# search_key = ...  # Key to search for
# result = bplus_tree.search(search_key)
