import mysql.connector
from config import *
from typing import *

def make_connection():
    conn = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DB

    )
    return conn


def create_table(cursor, TABLE_NAME):
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                    id int auto_increment primary key,
                    Restaurant_Name VARCHAR(100),
                    Res_Id VARCHAR(200),
                    Phone_No VARCHAR(200),
                    Full_Address VARCHAR(500),
                    Street_address VARCHAR(500),
                    City VARCHAR(200),
                    Country VARCHAR(100),
                    Region  VARCHAR(100),
                    Pincode VARCHAR(50),
                    Timing VARCHAR(400),
                    ETA     VARCHAR(100),
                    Map     VARCHAR(100),
                    Dining_Modes LONGTEXT,
                    Cuisions LONGTEXT,
                    Category LONGTEXT,
                    Featured_Category LONGTEXT,  
                    Currency VARCHAR(10)     

                    )


            """)
        print(f"Table {TABLE_NAME} Created!")
    except Exception as e:
        print("Error : ", create_table.__name__, e)

def batch_insert(cursor, con, insert_query: str, values: List[Tuple], batch_size: int = db_batches):

    total_records = len(values)
    batch_count = 0
    failed_batches = []

    for s in range(0, total_records, batch_size):

        e = min(s + batch_size, total_records)
        batch = values[s:e]

        try:
            cursor.executemany(insert_query, batch)
            con.commit()

            batch_count += 1
            print(f"Inserted batch {batch_count} ({s} -> {e})")

        except Exception as exp:
            print(f"Batch failed ({s} -> {e})")
            print("Error:", exp)
            failed_batches.append(batch)

    return batch_count, failed_batches

def insert_into_db(cursor,con, parsed_batch ,TABLE_NAME: str):


    try:
        if not parsed_batch:
            return

        # columns from first row
        cols = ",".join(parsed_batch[0].keys())

        # placeholders
        vals = ",".join(["%s"] * len(parsed_batch[0]))

        insert_query = f"""
        INSERT INTO {TABLE_NAME} ({cols})
        VALUES ({vals})
        ON DUPLICATE KEY UPDATE Res_Id =Res_Id
        """

        # convert dict rows → tuple values
        values = [tuple(row.values()) for row in parsed_batch]

        batch_insert(cursor, con, insert_query, values)

        print(f"{len(values)} Records Inserted Successfully")

    except Exception as e:
        print("Error:", insert_into_db.__name__, e)
