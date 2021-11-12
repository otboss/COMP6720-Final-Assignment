from model.File import File
from util.binary_io import write_to_binary_file, append_to_binary_file
import os

def create_table(tableName, fieldNames):#fieldNames is a list
    if os.path.exists(tableName):
         raise Exception("Table already exists")
    else:
        newtable= File(tableName)
        newtable.table_str(fieldNames)
        listToStr = ' '.join([str(elem) for elem in newtable])
        write_to_binary_file(tableName,listToStr)


