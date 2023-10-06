from database import *
from bplustree import *
import random
import timeit

################################# SETUP #################################

# Initialize the database file
db_file = DatabaseFile()
db_file.import_file("games.txt")

# populating a new instance of database since the old database has had records deleted
db_file_q5_brute_force = DatabaseFile()
db_file_q5_brute_force.import_file("games.txt")

bplustree = BPlusTree()

# toDel = set()
# recordSet = set()
for block_idx, block in enumerate(db_file.blocks):
    for record_idx, record in enumerate(block.data):
        # if record.FG_PCT_home <= 0.35:
        #     toDel.add(record.FG_PCT_home)
        # recordSet.add(record.FG_PCT_home)
        bplustree.insert(record.FG_PCT_home, [block_idx, record_idx])
# print("BEFORE:")
# bplustree.show()

# toDel = sorted(list(toDel))
# for i, val in enumerate(toDel):
#     # print(f"DELETE {val}")
#     bplustree.delete(val)
# print("AFTER:")
# bplustree.show()

# Calculate number of levels of tree. Necessary constant for Q2, 3, 4
numlevels = 1
node = bplustree.root
while not node.is_leaf:
    node = node.children[0]
    numlevels += 1

############################### PRINT EXPERIMENT RESULTS ###############################

# Q1 Storing data on disk
def q1_result():
    print("################### EXPERIMENT 1: STORING DATA ON DISK ####################")
    print("Number of records: ", db_file.num_records)   
    print("Size of a record: ", RECORD_SIZE)
    print("No. of records stored in a block: ", len(db_file.blocks[0].data))
    print("No. of blocks for storing data: ", len(db_file.blocks))


# second Q3 init b+ tree/insertion into b+ tree
# Q2 init b+ tree/insertion into b+ tree
def q2_result():
    print("################### EXPERIMENT 2: B+ TREE ####################")

    # Use BFS to calculate number of nodes
    numnode = 0
    bfs_q = [bplustree.root]
    while bfs_q:
        node = bfs_q.pop(0)
        numnode += 1
        if not node.is_leaf:
            bfs_q += node.children

    print(f"Value of N: {N}")
    print(f"No. Nodes of Tree: {numnode}")
    print(f"No. Levels of Tree: {numlevels}")
    print(f"Content of Root Node: {bplustree.root.keys}")


# Q3 query on index
def q3_indexquery(key = 0.5): # Pure index query, used for runtime measurement
    results = []
    records, c_idx = bplustree.search(key)
    
    for b_id, r_id in records:
        blk = db_file.read_block(b_id)
        results.append(blk.data[r_id].serialize())
    return results

def q3_bruteforce(key = 0.5): # Pure brute force query, used for runtime measurement
    results = []
    for blk in db_file.blocks:
        for record in blk.data:
            if record.FG_PCT_home == key:
                results.append(record.serialize())
    return results

# Calculates and prints necessary data for Q3
def q3_result():
    print("################### EXPERIMENT 3: INDEX QUERY ####################")
    timer1 = timeit.Timer(lambda:q3_indexquery())
    elapsed = timer1.timeit(1000) # Index query runtime

    timer2 = timeit.Timer(lambda:q3_bruteforce())
    elapsed_bf = timer2.timeit(1000) # Brute force query runtime

    results = []
    numblocks = set() # Number of datablocks accessed
    sum_fg3_pct_home = 0 # Sum of FG3_PCT_home results
    records, c_idx = bplustree.search(0.5)
    
    for b_id, r_id in records: # Iterate through results, calculate necessary data
        numblocks.add(b_id)
        rcd = db_file.read_block(b_id).data[r_id]
        sum_fg3_pct_home += rcd.FG3_PCT_home
        results.append(rcd.serialize())

    print('Query Results:', '\n'.join(results)) #uncomment to print
    print(f'No. Index Nodes Accessed: {numlevels+c_idx}')
    print(f'No. Datablocks Accessed (Index): {len(numblocks)}')
    print(f'Avg. FG3_PCT_home: {sum_fg3_pct_home/len(records):.2f}')
    print(f'Index Query Runtime: {elapsed/1000:.5f}s\n')

    print(f'No. Datablocks Accessed (Brute Force): {len(db_file.blocks)}') # must access all blocks
    print(f'Brute Force Runtime: {elapsed_bf/1000:.5f}s')


# Q4 range query on index
def q4_rangequery(key = 0.6, key2 = 1): # Pure range query for runtime measurement
    results = []
    records, c_idx = bplustree.search(key, key2)

    for b_id, r_id in records:
        blk = db_file.read_block(b_id)
        results.append(blk.data[r_id].serialize())
    return results
    
def q4_bruteforce(key = 0.6, key2 = 1): # Pure brute force query for runtime measurement
    results = []
    for blk in db_file.blocks:
        for record in blk.data:
            if key<=record.FG_PCT_home<=key2:
                results.append(record.serialize())
    return results

# Calculates and prints necessary data for Q4
def q4_result():
    print("################### EXPERIMENT 4: INDEX RANGE QUERY ####################")
    timer1 = timeit.Timer(lambda:q4_rangequery())
    elapsed = timer1.timeit(1000) # Index range query runtime

    timer2 = timeit.Timer(lambda:q4_bruteforce())
    elapsed_bf = timer2.timeit(1000) # Brute force range query runtime

    results = []
    numblocks = set() # Number of datablocks accessed
    sum_fg3_pct_home = 0 # Sum of FG3_PCT_home results
    records, c_idx = bplustree.search(0.6, 1)
    
    for b_id, r_id in records: # Iterate through results, calculate necessary data
        numblocks.add(b_id)
        rcd = db_file.read_block(b_id).data[r_id]
        sum_fg3_pct_home += rcd.FG3_PCT_home
        results.append(rcd.serialize())
    
    print('Query Results:', '\n'.join(results)) #uncomment to print
    print(f'No. Index Nodes Accessed: {numlevels+c_idx}')
    print(f'No. Datablocks Accessed (Index): {len(numblocks)}')
    print(f'Avg. FG3_PCT_home: {sum_fg3_pct_home/len(records):.2f}')
    print(f'Index Query Runtime: {elapsed/1000:.5f}s\n')

    print(f'No. Datablocks Accessed (Brute Force): {len(db_file.blocks)}') # must access all blocks
    print(f'Brute Force Runtime: {elapsed_bf/1000:.5f}s')


# Q5 range deletion
def q5_delete_records_using_tree():
    # search for records with 0 <= FG_PCT_home <= 0.35 to delete
    records, _ = bplustree.search(0, 0.35)

    keys_to_delete = set()

    # delete records from database and store keys to delete
    for b_id, r_id in records:
        cur_block = db_file.read_block(b_id)
        keys_to_delete.add(cur_block.data[r_id].FG_PCT_home)
        db_file.delete_record(b_id, r_id)

    # delete keys from b+ tree
    for key in keys_to_delete:
        bplustree.delete(key)

def q5_get_num_of_blocks():
    records, _ = bplustree.search(0, 0.35)
    unique_blocks = set()
    for b_id, r_id in records:
        unique_blocks.add(b_id)
    return len(unique_blocks)

def q5_bruteforce():
    for block_idx, block in enumerate(db_file_q5_brute_force.blocks):
        for record_idx, record in enumerate(block.data):
            if record and record.FG_PCT_home <= 0.35:
                db_file_q5_brute_force.delete_record(block_idx, record_idx)

def q5_result():
    print("################### EXPERIMENT 5: DELETE RECORDS “FG_PCT_home” <= 0.35 ####################")
    timer1 = timeit.Timer(lambda:q5_delete_records_using_tree())
    elapsed = timer1.timeit(1) # Index range query runtime

    # Calculate number of levels of tree. Necessary constant for Q2, 3, 4
    numlevels = 1
    node = bplustree.root
    while not node.is_leaf:
        node = node.children[0]
    numlevels += 1

    numnode = 0
    bfs_q = [bplustree.root]
    while bfs_q:
        node = bfs_q.pop(0)
        numnode += 1
        if not node.is_leaf:
            bfs_q += node.children

    print(f'Number of nodes in the updated B+ tree: {numnode}')
    print(f'Number of levels updated in B+ tree: {numlevels}')
    print(f'Root node of B+ tree contents: {bplustree.root.keys}')
    print(f'Runtime of process: {elapsed:.15f}ms')
    
    timer2 = timeit.Timer(lambda:q5_bruteforce())
    elapsed_bf = timer2.timeit(1) # Brute force range query runtime
    print(f'Number of blocks accessed by brute-force: {len(db_file.blocks)}')
    print(f'Brute Force Runtime: {elapsed_bf:.15f}ms')


################################# RUN TEST #################################
# q1_result()
# q2_result()
# q3_result()
# q4_result()
q5_result()
