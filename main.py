from database import *
from bplustree import *
import csv

# Define constants and configurations
BLOCK_SIZE = 400  # Block size in bytes
DISK_CAPACITY = 500 * 1024 * 1024  # Disk capacity in bytes (500 MB)
RECORD_SIZE = 5*8 + 3*8 + 8 #(5 ints, 8 bytes) + (3 floats, 8 bytes) + (size of datetime object)
# todo: change to sys.getsizeof(record_1)) or sys.getsizeof(record_1.serialize())
# todo: calculate size of N for size of a B+ tree node <= BLOCK_SIZE

# Calculate the number of records that can fit in a block
RECORDS_PER_BLOCK = BLOCK_SIZE // RECORD_SIZE
print("Records per block:", RECORDS_PER_BLOCK)

# Initialize the database file
db_file = DatabaseFile()
# record_1 = Record("22/12/2022", 1610612740, 126, 0.484, 0.926, 0.382, 25, 46, 1)
# print(sys.getsizeof(record_1))
# print(sys.getsizeof(record_1.serialize()))

# max serialize value should be 100
# record_2 = Record("22/12/2021", 1610612740, 126, 0.4, 0.926, 0.382, 25, 46, 1)
# print(sys.getsizeof(record_2))
# print(sys.getsizeof(record_2.serialize()))


with open("games.txt", "r", encoding="utf8") as games_file:
    games_reader = csv.DictReader(games_file, delimiter="\t")
    record_count = 0
    block = Block()
    for game in games_reader:
        first = game["GAME_DATE_EST"]
        second = game["TEAM_ID_home"]
        third = game["PTS_home"]
        fourth = game["FG_PCT_home"]
        fifth = game["FT_PCT_home"]
        sixth = game["FG3_PCT_home"]
        seventh = game["AST_home"]
        eighth = game["REB_home"]
        ninth = game["HOME_TEAM_WINS"]

        #ignore incomplete records
        if not (bool(third) and bool(third) and bool(fourth) and bool(fifth) and bool(sixth) and bool(seventh) and bool(eighth)):
            continue

        if record_count >= 5:
            db_file.blocks.append(block) # append block to databasefile
            db_file.num_records += 5
            block = Block() #create new block
            record_count = 0
        record = Record(first, int(second), int(third), float(fourth), float(fifth), float(sixth), int(seventh), int(eighth), int(ninth))
        record_count += 1
        block.data.append(record)
    
    db_file.blocks.append(block)
    db_file.num_records += len(block.data)

print(db_file.blocks[0].data[0].GAME_DATE_EST)
print(db_file.num_records)     
# Q3 todo: import actual data rows (clean then add)

# second Q3 init b+ tree/insertion into b+ tree

# Q4 query on index

# Q5 range query on index

# Q6 range deletion