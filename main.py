from database import *
from bplustree import *

# Define constants and configurations
BLOCK_SIZE = 400  # Block size in bytes
DISK_CAPACITY = 500 * 1024 * 1024  # Disk capacity in bytes (500 MB)
RECORD_SIZE = 64  # Size of a record in bytes; 
# todo: change to sys.getsizeof(record_1)) or sys.getsizeof(record_1.serialize())
# todo: calculate size of N for size of a B+ tree node <= BLOCK_SIZE

# Calculate the number of records that can fit in a block
RECORDS_PER_BLOCK = BLOCK_SIZE // RECORD_SIZE

# Initialize the database file
db_file = DatabaseFile()
record_1 = Record("22/12/2022", 1610612740, 126, 0.484, 0.926, 0.382, 25, 46, 1)
print(sys.getsizeof(record_1))
print(sys.getsizeof(record_1.serialize()))

# max serialize value should be 100
record_2 = Record("22/12/2021", 1610612740, 126, 0.4, 0.926, 0.382, 25, 46, 1)
print(sys.getsizeof(record_2))
print(sys.getsizeof(record_2.serialize()))

# Q3 todo: import actual data rows (clean then add)

# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion