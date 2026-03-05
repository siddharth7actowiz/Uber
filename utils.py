from marshal import loads

import json

def read_file(file_path):
    try:
            with open(file_path,"r")as f:
                python_data=json.load(f)
                return  python_data
    except Exception as e:
         print("Error:",read_file.__name__,e)    