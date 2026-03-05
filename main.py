import json
import os
import time
from config import *
from utils import *
from parser import prser
from db import make_connection, insert_into_db, create_table



def main():
    st=time.time()
    conn = make_connection()
    cursor = conn.cursor()

    create_table(cursor, TABLE_NAME)

    raw_json = read_file(file_path)

    json_data = prser(raw_json)

    insert_into_db(cursor, json_data,TABLE_NAME)

    conn.commit()
    conn.close()
    print("Total time:",time.time()-st) 

if __name__ == "__main__":
    main()