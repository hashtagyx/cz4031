import sys

# Define constants and configurations
BLOCK_SIZE = 400  # Block size in bytes
DISK_CAPACITY = 500 * 1024 * 1024  # Disk capacity in bytes (500 MB)
RECORD_SIZE = 5*8 + 3*8 + 8 #(5 ints, 8 bytes) + (3 floats, 8 bytes) + (size of datetime object)
# RECORD_SIZE = 64  # Size of a record in bytes
# Datetime, 5 integers, 3 floats/doubles
# !!! todo: find actual size of a record, using https://stackoverflow.com/a/33631772
# pympler library asizeof or sys.getsizeof()
# todo: calculate size of N for size of a B+ tree node <= BLOCK_SIZE

# Calculate the number of records that can fit in a block
RECORDS_PER_BLOCK = BLOCK_SIZE // RECORD_SIZE

# Create a data structure to represent a block
class Block:
    def __init__(self):
        self.data = []
        # self.data = bytearray(BLOCK_SIZE)
# // (GAME_DATE_EST 	TEAM_ID_home	PTS_home	FG_PCT_home	FT_PCT_home	FG3_PCT_home	AST_home	REB_home	HOME_TEAM_WINS)
# // Datetime, 5 integers, 3 floats/doubles e.g. 
# // 22/12/2022	1610612740	126	0.484	0.926	0.382	25	46	1
# Create a data structure to represent a record
class Record:
    def __init__(self, GAME_DATE_EST, TEAM_ID_home, PTS_home, FG_PCT_home, FT_PCT_home, FG3_PCT_home, AST_home, REB_home, HOME_TEAM_WINS):
        self.GAME_DATE_EST = GAME_DATE_EST # datetime
        self.TEAM_ID_home = TEAM_ID_home # int
        self.PTS_home = PTS_home # int
        self.FG_PCT_home = FG_PCT_home # double
        self.FT_PCT_home = FT_PCT_home # double
        self.FG3_PCT_home = FG3_PCT_home # double
        self.AST_home = AST_home # int
        self.REB_home = REB_home # int
        self.HOME_TEAM_WINS = HOME_TEAM_WINS # int

    # if we need to store it in a serialized format (e.g. byte string)
    # def serialize(self):
    #     # Serialize the record data to a fixed-length string
    #     record_data = [self.timestamp.strftime('%Y-%m-%d %H:%M:%S')] + \
    #                   [str(i) for i in self.integers] + \
    #                   [str(d) for d in self.doubles]
    #     return '|'.join(record_data).ljust(RECORD_SIZE)

    # @staticmethod
    # def deserialize(record_str):
    #     # Deserialize a string into a record object
    #     record_data = record_str.strip().split('|')
    #     timestamp = datetime.datetime.strptime(record_data[0], '%Y-%m-%d %H:%M:%S')
    #     integers = [int(i) for i in record_data[1:5]]
    #     doubles = [float(d) for d in record_data[5:]]
    #     return Record(timestamp, integers, doubles)

# Create a data structure to represent a database file
class DatabaseFile:
    def __init__(self):
        self.blocks = []  # List to store blocks
        self.num_records = 0  # Total number of records
        self.current_block = None  # Current block for writing

    def write_block(self, block):
        # Append a block to self.blocks, ensuring it doesn't exceed BLOCK_SIZE
        if len(block.data) <= BLOCK_SIZE:
            self.blocks.append(block)
        else:
            raise ValueError("Block size exceeds BLOCK_SIZE")
    
    def read_block(self, block_index):
        # Read a block from self.blocks by its index
        if block_index < 0 or block_index >= len(self.blocks):
            return None  # Invalid block_index

        return self.blocks[block_index]
    
    # leaves a hole in the block's records
    def delete_record(self, block_index, record_index):
        if block_index < 0 or block_index >= len(self.blocks):
            return  # Invalid block_index
        if record_index < 0 or record_index >= len(self.blocks[block_index]):
            return  # Invalid record_index
        self.blocks[block_index][record_index] = None

    # replaces the entire record with a hole
    def delete_block(self, block_index):
        if block_index < 0 or block_index >= len(self.blocks):
            return  # Invalid block_index
        self.blocks[block_index] = None

    # def create_new_block(self):
    #     # Create a new block and add it to the database file
    #     new_block = Block()
    #     self.blocks.append(new_block)
    #     self.current_block = new_block

    # def write_record(self, record):
    #     # Write a record to the database file
    #     if self.current_block is None or len(self.current_block.data) >= BLOCK_SIZE:
    #         self.create_new_block()

    #     # Serialize the record and write it to the current block
    #     serialized_record = record.serialize()
    #     offset = len(self.current_block.data)
    #     self.current_block.data[offset:offset + RECORD_SIZE] = serialized_record.encode('utf-8')

    #     self.num_records += 1

    # def read_record(self, record_id):
    #     # Read a record from the database file based on record_id
    #     if record_id < 0 or record_id >= self.num_records:
    #         return None  # Invalid record_id

    #     block_index = record_id // RECORDS_PER_BLOCK
    #     offset_within_block = (record_id % RECORDS_PER_BLOCK) * RECORD_SIZE

    #     block = self.blocks[block_index]
    #     record_data = block.data[offset_within_block:offset_within_block + RECORD_SIZE]

    #     return Record.deserialize(record_data.decode('utf-8'))

# Initialize the database file
db_file = DatabaseFile()

# todo: replace with actual data rows
# Sample usage
# timestamp = datetime.datetime(2023, 9, 22, 10, 30, 0)
# integers = [42, 123, -5, 0]
# doubles = [3.14, 2.718, -1.0, 0.0]
