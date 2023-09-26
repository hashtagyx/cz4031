from database import *
from bplustree import *
import random


# Initialize the database file
db_file = DatabaseFile()
db_file.import_file("games.txt")

print(db_file.blocks[0].data[0].GAME_DATE_EST)
print(db_file.num_records)     

bplustree = BPlusTree()
# random_list = random.sample(range(1, 100), 20)

random_list = [1,4,7,10,17,21,31,25,19,20,28,42]
for i in random_list:
    bplustree[i] = 'test' + str(i)
    print('Insert ' + str(i))
    bplustree.show()


# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion