from database import *
from bplustree import *
# from test import *
import random

random.seed(0)

# Initialize the database file
db_file = DatabaseFile()
db_file.import_file("games.txt")

bplustree = BPlusTree()

# for block_idx, block in enumerate(db_file.blocks):
#     for record_idx, record in enumerate(block.data):
#         # bplustree[record.FG_PCT_home] = [block_idx, record_idx]
#         bplustree.insert(record.FG_PCT_home, [block_idx, record_idx])
#         # print(block_idx, record_idx, record.FG_PCT_home)
# bplustree.show()
        

# random_list = random.sample(range(1, 100), 20)

# random_list = [1,4,7,7,10,17,22,31,25,20,21,28,42,7,7,7,18,19]
random_list = [1,4,7,10,17,22,31,25,20,21,28,42,51,100]
# random_list = random.sample(range(1, 1000), 200)
# random_list = [338, 771, 201, 672, 927, 902, 943, 116, 375, 446, 637, 213, 498, 687, 669, 464, 594, 974, 671, 151, 945, 143, 115, 233, 246, 237, 854, 503, 992, 389, 105, 807, 377, 749, 806, 189, 69, 84, 343, 775, 19, 712, 563, 376, 897, 991, 402, 825, 693, 798, 374, 471, 55, 912, 109, 388, 755, 583, 379, 507, 62, 870, 18, 842, 138, 970, 855, 663, 336, 882, 644, 819, 291, 77, 27, 410, 79, 694, 744, 888, 711, 297, 429, 688, 737, 529, 223, 4, 657, 123, 508, 732, 474, 846, 234, 849, 394, 723, 856, 765, 715, 691, 182, 829, 285, 519, 439, 990, 232, 956, 426, 76, 417, 11, 756, 432, 860, 545, 314, 638, 803, 49, 647, 449, 150, 533, 922, 786, 368, 972, 731, 542, 832, 949, 575, 169, 938, 746, 493, 538, 100, 676, 532, 872, 728, 763, 329, 609, 627, 1, 126, 843, 372, 573, 906, 787, 433, 128, 884, 564, 761, 334, 827, 824, 50, 968, 745, 706, 93, 107, 642, 877, 561, 327, 847, 250, 38, 754, 299, 540, 944, 971, 800, 268, 560, 873, 623, 502, 219, 491, 147, 430, 351, 242, 915, 215, 760, 574, 413, 236]
# random_list = [1,4,7,10,17,19,20,21,25,31]
# print(1 if 368 in random_list else 0)
for idx, i in enumerate(random_list):
    # bplustree[i] = [('idx:', idx, 'key:', i)]
    bplustree.insert(i, ('idx:', idx, 'key:', i))
    print('Insert ' + str(i))
    # bplustree.show()
bplustree.show()

# random.shuffle(random_list)
random_list = [10, 7,21, 17, 25, 22, 31, 28, 1, 100, 4]
# random_list = [446,712]
# random_list = [17,19, 4]

for idx, i in enumerate(random_list):
    print('Delete ' + str(i))
    bplustree.delete(i)
    bplustree.show()
    
bplustree.show()



# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion