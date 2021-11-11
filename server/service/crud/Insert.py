from util.binary_io import append_to_binary_file
import os

def insert_records (tableName, block):
    if os.path.exists(tableName):
        for i in block:
            listToStr = ' '.join([str(elem) for elem in i])
            append_to_binary_file(tableName, listToStr) # function add_to_binary to be created in binary_io that will be used to add to a existing file 
    else:
        raise Exception("Table Does not Exist")