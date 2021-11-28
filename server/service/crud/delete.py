import shutil
from typing import Set, List, Callable
from model.Record import Record
import util.crud_helpers as helper
import os
from util import working_directory
import util.binary_io as file_helper
import json

def drop_database(working_directory: str, database: str):
  if(working_directory[-1] != "/"):
    working_directory = working_directory + "/"
  shutil.rmtree(working_directory + database)

def drop_table(working_directory: str, database: str, table_name: str):
  if(working_directory[-1] != "/"):
    working_directory = working_directory + "/"
  os.remove(working_directory + database + "/" + table_name + ".bin")

def delete_records(dbName:str, tableName: str,filters: str):
    wd = working_directory.load_working_directory()
    file_path = wd + '/' + dbName + '/' + tableName

    if os.path.exists(file_path):
        #get file contents
        contents = file_helper.read_from_binary_file(file_path)
        contents_dict = json.loads(contents) #convert contents from json to dictionary


        #break down conditions into a list
        conditions_list =  helper.create_conds_lst(filters.split())

        #Evaluate each record
        select_lst = []
        
        for block in contents_dict["data_items"]:
            return_record : Record  = Record()
            projected_record = {}
            for record in block["records"]:
                result = helper.evaluate_conditions(conditions_list,record)
                if result:
                    select_lst = select_lst + [record] #list of records to be deleted


        #add method to write to file

    else:
        raise Exception("Table Does not Exist")  




  