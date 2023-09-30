from database import *
from bplustree import *


# Initialize the database file
db_file = DatabaseFile()

# print(db_file.blocks[0].data[0].GAME_DATE_EST)

# Q3 todo: import actual data rows (clean then add)
print("################### EXPERIMENT 1: STORING DATA ON DISK ####################")
db_file.import_file("games.txt")
print("Number of records:", db_file.num_records)   
print("Size of a record: ", RECORD_SIZE)
print("No. of records stored in a block:", len(db_file.blocks[0].data))
print("No. of blocks for storing data:", len(db_file.blocks))

# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion