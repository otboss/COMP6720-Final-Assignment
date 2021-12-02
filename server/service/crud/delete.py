import shutil
from typing import Set, List, Callable
from model.Record import Record
from model.Block import Block
from util import working_directory
import util.crud_helpers as helper
import os
import util.binary_io as file_helper
import util.working_directory

import json

def drop_database(database: str):
  working_dir = working_directory.load_working_directory()
  if(working_dir[-1] != "/"):
    working_dir = working_dir + "/"
  shutil.rmtree("%s%s",working_directory, database)

def drop_table(database: str, table_name: str):
  working_dir = working_directory.load_working_directory()
  if(working_dir[-1] != "/"):
    working_dir = working_dir + "/"
  file_helper.delete_binary_file("%s/%s/%s"%(working_dir, database, table_name))

def delete_records(database:str, table_name: str, filters: str):
    working_dir = util.working_directory.load_working_directory()
    table_path = working_dir + '/' + database + '/' + table_name

    if os.path.exists("%s.bin"%(table_path)):
        #get file contents
        contents = file_helper.read_from_binary_file(table_path)
        #convert contents from json to dictionary
        contents_dict = json.loads(contents)

        #break down conditions into a list
        conditions_list =  helper.create_conds_lst(filters[0].split() if len(filters) > 0 else [])

        if len(conditions_list) != 0:
          for block in contents_dict["data_items"]:
              for record in block["records"]:
                result = helper.evaluate_conditions(conditions_list,record)
                if result:
                    block["records"].remove(record)
        else:
          #removing all records
          contents_dict["data_items"] = [] 

        #writing data to file
        file_helper.write_to_binary_file(table_path, json.dumps(contents_dict))
    else:
        raise Exception("Table Does not Exist")  
    
  