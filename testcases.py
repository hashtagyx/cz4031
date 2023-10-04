# TEST CASE 1: DELETE SIMPLE CASE WITH INTERNAL NODE REPLACEMENT (CASE 1, EASY CASE)
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25]
#       |- [20, 21, 22]
#       `- [25, 31]
# AFTER:
# `- [21]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25]
#       |- [21, 22]
#       `- [25, 31]
# levels = [
#     [[20]],
#     [[7,17], [25]],
#     [[1,4], [7,10], [17,19], [20,21,22], [25,31]]
# ]

# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(20)
# tree.show()

# TEST CASE 2: BORROW LEFT LEAF NODE (CASE 2)
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4, 5]
#    |  |- [7, 10, 16]
#    |  `- [17, 19]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# EXPECTED:
# `- [20]
#    |- [7, 16]
#    |  |- [1, 4, 5]
#    |  |- [7, 10]
#    |  `- [16, 19]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# levels = [
#     [[20]],
#     [[7,17], [25]],
#     [[1,4,5], [7,10,16], [17,19], [20,21], [25,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(17)
# tree.show()

# TEST CASE 3: BORROW RIGHT LEAF NODE (CASE 2)
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4, 5]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31, 32]
# AFTER:
# `- [21]
#    |- [7, 17]
#    |  |- [1, 4, 5]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [31]
#       |- [21, 25]
#       `- [31, 32]
# levels = [
#     [[20]],
#     [[7,17], [25]],
#     [[1,4,5], [7,10], [17,19], [20,21], [25,31,32]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(20)
# tree.show()

# TEST CASE 4: MERGE RIGHT LEAF NODE (CASE 3 NO RECURSION UPWARDS)
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# =========================================
# AFTER:
# `- [20]
#    |- [17]
#    |  |- [1, 7, 10]
#    |  `- [17, 19]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# levels = [
#     [[20]],
#     [[7,17], [25]],
#     [[1,4], [7,10], [17,19], [20,21], [25,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(4)
# tree.show()

# TEST CASE 5: MERGE RIGHT LEAF NODE (CASE 3 NO RECURSION UPWARDS) CHECK CHILDREN AND NEXT POINTERS
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25, 35]
#       |- [20, 21]
#       |- [25, 31]
#       `- [35, 36]
# =========================================
# AFTER:
# `- [21]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [35]
#       |- [21, 25, 31]
#       `- [35, 36]
# levels = [
#     [[20]],
#     [[7,17], [25, 35]],
#     [[1,4], [7,10], [17,19], [20,21], [25,31], [35,36]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(20)
# tree.show()

# TEST CASE 6: MERGE LEFT LEAF NODE (CASE 3 NO RECURSION UPWARDS)
# BEFORE:
# `- [20]
#    |- [7, 17]
#    |  |- [1, 4]
#    |  |- [7, 10]
#    |  `- [17, 19]
#    `- [25, 35]
#       |- [20, 21]
#       |- [25, 31]
#       `- [35, 36]
# =========================================
# AFTER:
# `- [20]
#    |- [7]
#    |  |- [1, 4]
#    |  `- [7, 10, 19]
#    `- [25, 35]
#       |- [20, 21]
#       |- [25, 31]
#       `- [35, 36]
# levels = [
#     [[20]],
#     [[7,17], [25, 35]],
#     [[1,4], [7,10], [17,19], [20,21], [25,31], [35,36]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(17)
# tree.show()

# TEST CASE 7: MERGE WITH LEFT INTERNAL NODE
# BEFORE:
# `- [17]
#    |- [7, 10, 13]
#    |  |- [1, 4]  
#    |  |- [7, 9]  
#    |  |- [10, 11]
#    |  `- [13, 16]
#    `- [25]       
#       |- [17, 21]
#       `- [25, 31]
# =========================================
# AFTER:
# `- [13]
#    |- [7, 10]
#    |  |- [1, 4]
#    |  |- [7, 9]
#    |  `- [10, 11]
#    `- [21]
#       |- [13, 16]
#       `- [21, 25, 31]

# levels = [
#     [[17]],
#     [[7,10,13], [25]],
#     [[1,4], [7,9], [10, 11], [13,16], [17,21], [25,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(17)
# tree.show()

# TEST CASE 7: MERGE WITH RIGHT INTERNAL NODE
# BEFORE:
# `- [17]
#    |- [7]
#    |  |- [1, 4]
#    |  `- [7, 8]
#    `- [25, 30]
#       |- [17, 19]
#       |- [25, 26]
#       `- [30, 31]
# =========================================
# AFTER:
# `- [25]
#    |- [17]
#    |  |- [1, 4, 8]
#    |  `- [17, 19]
#    `- [30]
#       |- [25, 26]
#       `- [30, 31]
# levels = [
#     [[17]],
#     [[7], [25,30]],
#     [[1,4], [7,8], [17, 19], [25,26], [30,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(7)
# tree.show()

# TEST CASE 8: REDUCE TREE LEVEL BY 1
# BEFORE:
# `- [20]
#    |- [7]
#    |  |- [1, 4]
#    |  `- [7, 10]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# =========================================
# AFTER:
# `- [20, 25]
#    |- [1, 7, 10]
#    |- [20, 21]
#    `- [25, 31]
# levels = [
#     [[20]],
#     [[7], [25]],
#     [[1,4], [7,10], [20, 21], [25,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# tree.delete(4)
# tree.show()

# TEST CASE 9: DELETING THE WHOLE TREE (INCLUDING DELETING KEY NOT IN TREE)
# BEFORE:
# `- [20]
#    |- [7]        
#    |  |- [1, 4]  
#    |  `- [7, 10] 
#    `- [25]       
#       |- [20, 21]
#       `- [25, 31]
# =========================================
# AFTER:
# DELETE 32
# INVALID KEY 32, NOT IN LEAF.KEYS [25, 31]
# `- [20]
#    |- [7]
#    |  |- [1, 4]
#    |  `- [7, 10]
#    `- [25]
#       |- [20, 21]
#       `- [25, 31]
# DELETE 1
# `- [20, 25]
#    |- [4, 7, 10]
#    |- [20, 21]
#    `- [25, 31]
# DELETE 4
# `- [20, 25]
#    |- [7, 10]
#    |- [20, 21]
#    `- [25, 31]
# DELETE 7
# `- [25]
#    |- [10, 20, 21]
#    `- [25, 31]
# DELETE 10
# `- [25]
#    |- [20, 21]
#    `- [25, 31]
# DELETE 20
# `- [21, 25, 31]
# DELETE 21
# `- [25, 31]
# DELETE 25
# `- [31]
# DELETE 31
# `- []
# levels = [
#     [[20]],
#     [[7], [25]],
#     [[1,4], [7,10], [20, 21], [25,31]]
# ]
# tree = constructor.construct_tree(levels)
# print('BEFORE:')
# tree.show()
# print('=========================================')
# print('AFTER:')
# toDelete = [32,1,4,7,10,20,21,25,31]
# for val in toDelete:
#     print(f"DELETE {val}")
#     tree.delete(val)
#     tree.show()

# TEST CASE 10: EXPERIMENT 5
bplustree = BPlusTree()

toDel = set()
for block_idx, block in enumerate(db_file.blocks):
    for record_idx, record in enumerate(block.data):
        # bplustree[record.FG_PCT_home] = [block_idx, record_idx]
        if record.FG_PCT_home <= 0.35:
            toDel.add(record.FG_PCT_home)
        bplustree.insert(record.FG_PCT_home, [block_idx, record_idx])
        # print(block_idx, record_idx, record.FG_PCT_home)
bplustree.show()

toDel = sorted(list(toDel))
for i, val in enumerate(toDel):
    print(f"DELETE {val}")
    bplustree.delete(val)
bplustree.show()