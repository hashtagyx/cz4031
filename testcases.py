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
