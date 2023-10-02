#DECLARE CONSTANTS
BLOCK_SIZE = 400  # Block size in bytes
DISK_CAPACITY = 500 * 1024 * 1024  # Disk capacity in bytes (500 MB)
RECORD_SIZE = 5*8 + 3*8 + 8 #(5 ints, 8 bytes) + (3 floats, 8 bytes) + (size of datetime object)
# N = 16 # N * (Cost of key) + (N+1) * (Cost of pointer) <= B ==> N*8 + (N+1)*16 <= 400 ==> N = 16
N = 16