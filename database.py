import sys
import csv
from datetime import datetime
from constant import *


# Calculate the number of records that can fit in a block
RECORDS_PER_BLOCK = BLOCK_SIZE // RECORD_SIZE

# Create a data structure to represent a block
class Block:
    def __init__(self):
        self.data = []
         # self.data = bytearray(BLOCK_SIZE)
        self.deleted = False

    # this block is now deleted
    def delete(self):
        self.deleted = True
       
# // (GAME_DATE_EST 	TEAM_ID_home	PTS_home	FG_PCT_home	FT_PCT_home	FG3_PCT_home	AST_home	REB_home	HOME_TEAM_WINS)
# // Datetime, 5 integers, 3 floats/doubles e.g. 
# // 22/12/2022	1610612740	126	0.484	0.926	0.382	25	46	1
# Create a data structure to represent a record
class Record:
    def __init__(self, GAME_DATE_EST, TEAM_ID_home, PTS_home, FG_PCT_home, FT_PCT_home, FG3_PCT_home, AST_home, REB_home, HOME_TEAM_WINS):
        self.GAME_DATE_EST = GAME_DATE_EST
        self.TEAM_ID_home = TEAM_ID_home # int
        self.PTS_home = PTS_home # int
        self.FG_PCT_home = FG_PCT_home # double
        self.FT_PCT_home = FT_PCT_home # double
        self.FG3_PCT_home = FG3_PCT_home # double
        self.AST_home = AST_home # int
        self.REB_home = REB_home # int
        self.HOME_TEAM_WINS = HOME_TEAM_WINS # int
    
    def serialize(self):
        # Serialize the record data to a fixed-length string
        record_data = [str(self.GAME_DATE_EST), str(self.TEAM_ID_home), str(self.PTS_home), str(self.FG_PCT_home), str(self.FT_PCT_home), str(self.FG3_PCT_home), str(self.AST_home), str(self.REB_home), str(self.HOME_TEAM_WINS)]
        return '|'.join(record_data)

# Create a data structure to represent a database file
class DatabaseFile:
    def __init__(self):
        self.blocks = []  # List to store blocks
        self.num_records = 0  # Total number of records
        self.current_block = None  # Current block for writing
    
    def import_file(self, file_path):
        with open(file_path, "r", encoding="utf8") as games_file:
            games_reader = csv.DictReader(games_file, delimiter="\t")
            record_count = 0
            block = Block()
            for game in games_reader:
                game_date_est = game["GAME_DATE_EST"]
                team_id_home = game["TEAM_ID_home"]
                pts_home = game["PTS_home"]
                fg_pct_home = game["FG_PCT_home"]
                ft_pct_home = game["FT_PCT_home"]
                fg3_pct_home = game["FG3_PCT_home"]
                ast_home = game["AST_home"]
                reb_home = game["REB_home"]
                home_team_wins = game["HOME_TEAM_WINS"]

                #ignore incomplete records
                if not (bool(game_date_est) and bool(team_id_home) and bool(pts_home) and \
                        bool(fg_pct_home) and bool(ft_pct_home) and bool(fg3_pct_home) and \
                        bool(ast_home) and bool(reb_home) and bool(home_team_wins)):
                    continue

                if record_count >= RECORDS_PER_BLOCK:
                    self.blocks.append(block) # append block to databasefile
                    self.num_records += RECORDS_PER_BLOCK
                    block = Block() #create new block
                    record_count = 0
                record = Record(game_date_est, int(team_id_home), int(pts_home), \
                                float(fg_pct_home), float(ft_pct_home), float(fg3_pct_home), \
                                int(ast_home), int(reb_home), int(home_team_wins))
                record_count += 1
                block.data.append(record)
            
            self.blocks.append(block)
            self.num_records += len(block.data)
    
    def write_block(self, block):
        # Append a block to self.blocks, ensuring it doesn't exceed BLOCK_SIZE
        if sys.getsizeof(block) <= BLOCK_SIZE:
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
        if block_index < 0 or block_index >= len(self.blocks) or self.blocks[block_index].deleted:
            print('delete_record: Invalid block_index or block is already deleted')
            return  # Invalid block_index or block is already deleted
        if record_index < 0 or record_index >= len(self.blocks[block_index]):
            print('delete_record: Invalid record_index')
            return  # Invalid record_index
        self.blocks[block_index][record_index] = None

    # replaces the entire record with a hole
    def delete_block(self, block_index):
        if block_index < 0 or block_index >= len(self.blocks):
            print('delete_block: Invalid block_index')
            return  # Invalid block_index
        self.blocks[block_index].delete()
