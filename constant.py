#DECLARE CONSTANTS
BLOCK_SIZE = 400  # Block size in bytes
DISK_CAPACITY = 500 * 1024 * 1024  # Disk capacity in bytes (500 MB)
RECORD_SIZE = 5*8 + 3*8 + 8 #(5 ints, 8 bytes) + (3 floats, 8 bytes) + (size of datetime object)
# N =  # todo: define N
# todo: change to sys.getsizeof(record_1)) or sys.getsizeof(record_1.serialize())
# todo: calculate size of N for size of a B+ tree node <= BLOCK_SIZE