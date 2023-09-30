from database import *
from bplustree import *
import random


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

random_list = [1,4,7,7,10,17,22,31,25,20,21,28,42,7,7,7,18,19]
for idx, i in enumerate(random_list):
    # bplustree[i] = [('idx:', idx, 'key:', i)]
    bplustree.insert(i, ('idx:', idx, 'key:', i))
    print('Insert ' + str(i))
    bplustree.show()


# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion