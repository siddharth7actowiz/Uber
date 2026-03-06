import json
import os
import time
from config import *
from utils import *
from parser import prser
from db import make_connection, insert_into_db, create_table



def main():
    srt = int(sys.argv[1])
    lt = int(sys.argv[2])
    st=time.time()
    conn = make_connection()
    cursor = conn.cursor()

    create_table(cursor, TABLE_NAME)

   parsed_batch = []
    # for parsing a file at a time
    for raw_json in load_files(DATA_DIR, srt, lt):

        try:
            parsed = prser(raw_json)
        except Exception as e:
            print("Parser Error:", e)
            continue

        if not parsed:
            continue

        parsed_batch.append(parsed)
        #inserting batches upto 500
        if len(parsed_batch) >= 500:
            insert_into_db(cursor, con, parsed_batch, TABLE_NAME)
            parsed_batch.clear()

    if parsed_batch:
        insert_into_db(cursor, con, parsed_batch, TABLE_NAME)

    conn.commit()
    conn.close()
    print("Total time:",time.time()-st) 

if __name__ == "__main__":

    main()
