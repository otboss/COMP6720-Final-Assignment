from typing import Set, List, Callable
from model.Record import Record
from model.Schema import Schema
from util import working_directory
from model.File import File
import util.crud_helpers as crud_helpers
import os
import util.binary_io
import json
import hashlib

def select_records(database_name:str, table_name: str, selectors: list[str], filters: list[str]) -> list[dict]:
    working_dir = working_directory.load_working_directory()
    table_path = "%s/%s/%s"%(working_dir, database_name, table_name)

    #TODO: Fix bugs

    if os.path.exists("%s.bin"%(table_path)):
        #get file contents
        contents = util.binary_io.read_from_binary_file(table_path)
        contents_dict = json.loads(contents) #convert contents from json to dictionary

        #store slectors as projections
        projections = selectors
        #break down conditions into a list
        conditions_list =  crud_helpers.create_conds_lst(filters[0].split() if len(filters) > 0 else [])

        #Evaluate each record
        select_lst = []

        # TODO: Implement index usage, search for existing indices for 
        # table and use for faster queries      
        
        for block in contents_dict["data_items"]:
            for record in block["records"]:
                return_record = {}
                projected_record = {}                
                if len(conditions_list) != 0:
                    record_matches = crud_helpers.evaluate_conditions(conditions_list, record)
                    if record_matches:
                        for projection in projections:
                            projected_record[projection] =  record[projection]
                        return_record = projected_record
                        select_lst = select_lst + [return_record]
                else:
                    for projection in projections:
                        projected_record[projection] =  record[projection]
                    return_record = projected_record
                    select_lst = select_lst + [return_record]          

        return select_lst
    raise Exception("Table Does not Exist")  


def describe_table(database_name: str, table_name: str) -> list[Schema]: 
    working_dir = working_directory.load_working_directory()
    table_path = "%s/%s/%s"%(working_dir, database_name, table_name)
    if os.path.exists("%s.bin"%(table_path)):
        contents: File = File.from_dict(json.loads(util.binary_io.read_from_binary_file(table_path)))
        return contents.schema
    raise Exception("Table Does not Exist")

def show_databases() -> list[str]: 
    working_dir = working_directory.load_working_directory()
    return os.listdir(working_dir)

def show_tables(database_name: str) -> list[str]: 
    working_dir = working_directory.load_working_directory()
    database_folder_contents = os.listdir("%s/%s"%(working_dir, database_name))
    tables: list[str] = []
    for content in database_folder_contents:
        if content[-4:] == ".bin" and content[0] != ".":
          tables.append(content[0:-4])
    return tables