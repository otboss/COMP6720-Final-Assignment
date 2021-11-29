import shutil
from typing import Set, List, Callable
from model.Record import Record
from model.Block import Block
from util import working_directory
import util.crud_helpers as helper
import os
import util.binary_io as file_helper
import json

def drop_database(database: str):
  working_dir = working_directory.load_working_directory()
  if(working_dir[-1] != "/"):
    working_dir = working_dir + "/"
  shutil.rmtree(working_directory + database)

def drop_table(database: str, table_name: str):
  working_dir = working_directory.load_working_directory()
  if(working_dir[-1] != "/"):
    working_dir = working_dir + "/"
  os.remove(working_directory + database + "/" + table_name + ".bin")

def delete_records(database:str, table_name: str,filters: str):
    working_dir = working_directory.load_working_directory()
    file_path = "%s/%s/%s"%(working_dir, database, table_name)

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
                    block["records"].remove(record)                    
                    #return_record = Record(list(record.keys()),list(record.values()))
                    #select_lst = select_lst + [return_record] #list of records to be deleted



        # length = len(select_lst)
        # if length%5 > 0:
        #     number_of_blocks = (length/5) + 1
        # else:
        #     number_of_blocks = (length/5)

        # blocks_lst = Create_Blocks(length, select_lst)


        # #create new file
        # new_file : File = File(contents_dict["table_name"],contents_dict["schema"])
        
        # for block in blocks_lst:
        #     new_file.add_block(block)

        # file_helper.write_to_binary_file( new_file.to_dict())

        file_helper.write_to_binary_file( contents_dict)

        

        #add method to write to file

    else:
        raise Exception("Table Does not Exist")  



def Create_Blocks(count,lst):
            blocks_lst = []
            if(count == 1):
                block : Block =  Block()
                length = len(lst)
                for record in lst[0:length]:
                    block.add_record(record)
                return [block]
            else:
              block : Block =  Block()
              for record in lst[0:5]:
                  block.add_record(record)
              blocks_lst = blocks_lst + [block] + Create_Blocks((count -1), lst[5:])
              return blocks_lst 
    
  