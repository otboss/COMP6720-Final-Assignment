from typing import Set, List, Callable
from model.Record import Record
from model.Schema import Schema
from util import working_directory
from model.File import File
import util.crud_helpers as crud_helpers
import os
import util.binary_io
import json


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
        conditions_list =  crud_helpers.create_conds_lst(filters)

        #Evaluate each record
        select_lst = []
        
        print("OK HERE! ")
        for block in contents_dict["data_items"]:
            return_record: Record
            projected_record = {}
            for record in block["records"]:
                result = crud_helpers.evaluate_conditions(conditions_list, record)
                if result:
                    for projection in projections:
                        projected_record[projection] =  record[projection]
                    return_record = Record.from_dict(projected_record)
                    select_lst = select_lst + [return_record]

        return select_lst
        
        #return select_lst

        # return_table = {record for record in contents_split if all(cond(record) for cond in conditions)}
        # return return_table 
    raise Exception("Table Does not Exist")  


def describe_table(database_name:str, table_name: str) -> list[Schema]: 
    working_dir = working_directory.load_working_directory()
    table_path = "%s/%s/%s"%(working_dir, database_name, table_name)
    if os.path.exists("%s.bin"%(table_path)):
        contents: File = File.from_dict(json.loads(util.binary_io.read_from_binary_file(table_path)))
        return contents.schema
    raise Exception("Table Does not Exist")

def show_databases() -> list[str]: 
    working_dir = working_directory.load_working_directory()
    return os.listdir(working_dir)