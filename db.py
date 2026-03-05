import mysql.connector
from config import *
def make_connection():
    conn=mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DB

    )
    return conn

def create_table(cursor,TABLE_NAME):
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                    id int auto_increment primary key,
                    Restaurant_Name VARCHAR(100),
                    Phone_No VARCHAR(20),
                    Full_Address VARCHAR(100),
                    Street_address VARCHAR(100),
                    City VARCHAR(20),
                    Country VARCHAR(10),
                    Region  VARCHAR(10),
                    Pincode SMALLINT,
                    ETA     VARCHAR(100),
                    Map     VARCHAR(100),
                    Dining_Modes TEXT,
                    Cuisions TEXT,
                    Category TEXT,
                    Featured_Category TEXT,  
                    Currency VARCHAR(10)     
                    
                    )


            """)
        print(f"Table {TABLE_NAME} Created!")
    except Exception as e:
        print("Error : ",create_table.__name__,e)    


def insert_into_db(cursor,data:dict,TABLE_NAME:str):
    try:
        cols=",".join(data.keys())
        vals=",".join(["%s"]*len(data))
        

        insert_query=f'''
            INSERT INTO {TABLE_NAME} ({cols}) VALUES ({vals})
            '''
        cursor.execute(insert_query,tuple(data.values()))
        print("Data Inserted Sussesfully")

    except Exception as e:
        print("Error:",insert_into_db.__name__,e)    
    