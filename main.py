from database import *
from bplustree import *


# Initialize the database file
db_file = DatabaseFile()
db_file.import_file("games.txt")

print(db_file.blocks[0].data[0].GAME_DATE_EST)
print(db_file.num_records)     
# Q3 todo: import actual data rows (clean then add)

# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion