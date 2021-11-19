from model.File import File
from util.binary_io import write_to_binary_file, append_to_binary_file
import util.working_directory
import model.Block
import os


def create_database(database_name: str):
    try:
        util.working_directory.create_sub_folder(database_name)
    except:
        pass

def create_table(table_name: str, field_names):#field_names is a list
    if os.path.exists(table_name):
         raise Exception("Table already exists")
    else:
        newtable= File(table_name)
        newtable.table_str(field_names)
        listToStr = ' '.join([str(elem) for elem in newtable])
        write_to_binary_file(table_name,listToStr)

def insert_records (table_name: str, block: model.Block):
    if os.path.exists(table_name):
        for i in block:
            listToStr = ' '.join([str(elem) for elem in i])
            append_to_binary_file(table_name, listToStr) # function add_to_binary to be created in binary_io that will be used to add to a existing file 
    else:
        raise Exception("Table Does not Exist")
