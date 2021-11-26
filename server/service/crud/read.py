from typing import Set, List, Callable
from model.Record import Record
import crud_helpers as helper
import os
from server.util import working_directory
import util.binary_io as file_helper
import json


def select(dbName:str, tableName: str, selectors: list[str], filters: str) -> list[Record]:
    wd = working_directory.load_working_directory()
    file_path = wd + '/' + dbName + '/' + tableName

    if os.path.exists(file_path):
        #get file contents
        contents = file_helper.read_from_binary_file(file_path)
        contents_dict = json.loads(contents) #convert contents from json to dictionary

        #store slectors as projections
        projections = selectors

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
                    for projection in projections:
                        projected_record[projection] =  record[projection]
                    return_record = Record.from_dict(projected_record)
                    select_lst = select_lst + [return_record]

        return select_lst
        
        #return select_lst

        # return_table = {record for record in contents_split if all(cond(record) for cond in conditions)}
        # return return_table 
    else:
        raise Exception("Table Does not Exist")  





def select_records(db_name:str, table_name: str, selectors: list[str] , filters: list[str]) -> list[Record]:
    pass



def show_databases(working_directory: str) -> list[str]: 
  return os.listdir(working_directory)