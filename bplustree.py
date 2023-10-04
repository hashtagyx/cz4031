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
        
        print('cur', node) 
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
        else:
            # print('children', node.children)
            print('next', node.next)

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

    # returns the path of nodes travelled to reach the leaf node which should contain this key
    def findPath(self, key):
        path = []
        node = self.root
        while not node.is_leaf:
            path.append(node)
            node = node.children[node.index(key)]
        path.append(node)
        return path
    
    # this function replaces the popped value with the newMinInLeaf 
    # if the popped value exists along the path to the leaf
    def updateInternalNodes(self, path, popped, newMinInLeaf):
        while path:
            curNode = path.pop()
            if popped in curNode.keys:
                i = curNode.keys.index(popped)
                curNode.keys[i] = newMinInLeaf
                return
    
    def delete(self, key):
        # Delete the key in the B+ tree and the array that the last layer points to
        leaf = self.find(key)
        path = self.findPath(key)
        if key not in leaf.keys:
            print(f"INVALID KEY {key}, NOT IN LEAF.KEYS {leaf.keys}")
            return
        
        # remove the key and its child from the leaf node.
        i = leaf.keys.index(key)
        popped = leaf.keys.pop(i)
        leaf.children.pop(i)

        # if the leaf node is the root, we are done with this deletion
        if self.root == leaf:
            return
        
        # case 1: we can remove the key from the tree directly. update the internal nodes if we deleted a key used in an internal node.
        if len(leaf.keys) >= MIN_LEAF:
            newMinInLeaf = leaf.keys[0]
            print("CASE 1: BEFORE UPDATE INTERNAL NODES")
            self.show()
            self.updateInternalNodes(path, popped, newMinInLeaf)
            print("=======================================")
            print("CASE 1: AFTER UPDATE INTERNAL NODES")
            self.show()
            return
        # case 2: we try to borrow a key from a neighbour. if it's successful, we are done
        elif self.borrowKey(path, popped):
            print("BORROWED SUCCESSFULLY")
            return
        
        rKey, rChild, mergedNode = self.mergeLeaf(path, popped)
        if len(path[-2].keys) < MIN_INTERNAL:
            # self.fixInternal(path[:-1], rKey)
            pass
        newPath = self.findPath(mergedNode.keys[0])
        self.updateInternalNodes(newPath, popped, mergedNode.keys[0])
        return

    def borrowKey(self, path, popped):
        leafNode = path[-1]
        oldMinInLeaf = popped
        # finding the old minimum value in the leaf node so that we can updateInternalNodes later
        if leafNode.keys and leafNode.keys[0] < popped:
            oldMinInLeaf = leafNode.keys[0]

        # this is the parent of the leaf node, which definitely exists since this leaf node
        # is not the root node as checked earlier in delete
        parent = path[-2]

        # get the index of our leaf's leftSibling
        i = parent.keys.index(oldMinInLeaf) if oldMinInLeaf in parent.keys else -1

        # define siblings; note that parent.children[i+1] is leafNode
        leftSibling = parent.children[i] if i >= 0 else None
        rightSibling = parent.children[i+2] if i+2 < len(parent.children) else None

        # try to borrow from left sibling
        if leftSibling and len(leftSibling.keys) > MIN_LEAF:
            # borrow from leftSibling's keys and children
            leafNode.keys.insert(0, leftSibling.keys.pop())
            leafNode.children.insert(0, leftSibling.children.pop())
            # update the internal nodes if required. old value = oldMinInLeaf, new value = borrowed key from leftSibling
            self.updateInternalNodes(path[:-1], oldMinInLeaf, leafNode.keys[0])
            return True
        
        # try to borrow from right sibling since we can't from left sibling
        if rightSibling and len(rightSibling.keys) > MIN_LEAF:
            leafNode.keys.append(rightSibling.keys.pop(0))
            leafNode.children.append(rightSibling.children.pop(0))
            # update our rightSibling's parent since we borrowed their previous smallest key
            self.updateInternalNodes(path[:-1], leafNode.keys[-1], rightSibling.keys[0])
            # update our leafNode's parent/internal node along path if we deleted the oldMinInLeaf
            # note: oldMinInLeaf could still be in the leaf node. however, it won't be if oldMinInLeaf == popped.
            # this function replaces the second argument with the third argument along the path,
            # however it does nothing if the second argument isn't along the path
            self.updateInternalNodes(path[:-1], oldMinInLeaf, leafNode.keys[0])
            return True
        
        # we did not manage to borrow from our siblings as a leaf. we now need to do merging.
        return False
    
    def mergeLeaf(self, path, popped):
        leaf = path[-1]
        parent = path[-2]
        # finding the old minimum value in the leaf
        oldMinInLeaf = popped
        if leaf.keys and leaf.keys[0] < oldMinInLeaf:
            oldMinInLeaf = leaf.keys[0]

        # using oldMinInLeaf to check if the node that we are going to delete (merge) {there are other ways we can do this, e.g. bisect_right(parent.keys, popped) to find the index of the leaf node in parent.children}
        # is the zeroth child or not. if it is, the zeroth child, we need to merge right.
        # otherwise, we can merge with the left node.

        # merging left if we can
        if oldMinInLeaf in parent.keys:
            # finding the index of the key to remove from parent and the leftSibling
            i = parent.keys.index(oldMinInLeaf)
            leftSibling = parent.children[i]

            # merge with leftSibling, and assign new next node for the leftSibling
            newNextNode = leaf.next
            leftSibling.keys += leaf.keys
            leftSibling.children += leaf.children
            leftSibling.next = newNextNode

            # removing the key and child in our parent node now that the node has been merged
            removedKey = parent.keys.pop(i)
            removedChild = parent.children.pop(i+1)
            mergedNode = leftSibling
        # we need to merge right, since leaf is the zeroth child
        else:
            rightSibling = parent.children[1]
            # finding the prev leaf by using self.find, but subtracting a fraction from the oldMinInLeaf so we get the direct prev node instead of the same node
            prevLeaf = self.find(oldMinInLeaf - 0.0001)
            # there exists a case where prevLeaf == leaf, but this is harmless
            prevLeaf.next = leaf.next

            rightSibling.keys = leaf.keys + rightSibling.keys
            rightSibling.children = leaf.children + rightSibling.children
            removedKey = parent.keys.pop(0)
            removedChild = parent.children.pop(0)
            mergedNode = rightSibling
            # self.updateInternalNodes() don't need to do so as it's handled by delete()
    
        return removedKey, removedChild, mergedNode
        


class BPlusTreeConstructor:
    def __init__(self):
        self.tree = BPlusTree()

    def construct_tree(self, levels):
        if not levels:
            raise ValueError("Levels list cannot be empty")

        tree = BPlusTree()
        childrenNodes = []
        for i in range(len(levels) - 1, -1, -1):
            curNodes = []
            for node in levels[i]:
                curNode = BPlusTreeNode()
                curNode.keys = node
                curNode.children = []
                for _ in range(len(curNode.keys) + 1):
                    if not childrenNodes:
                        if i != len(levels) - 1:
                            print(f'LEVEL {i}, NOT ENOUGH CHILDREN')
                        break
                    curNode.children.append(childrenNodes.pop(0))
                curNodes.append(curNode)
            
            # add dummy children and next pointer since this is leaf level
            if i == len(levels) - 1:
                for node in curNodes:
                    # dummy children
                    node.children = [(val, val) for val in node.keys]
                    node.is_leaf = True
                for j in range(len(curNodes) - 1):
                    curNodes[j].next = curNodes[j+1]
            
            childrenNodes = curNodes
        tree.root = childrenNodes[0]
        return tree
