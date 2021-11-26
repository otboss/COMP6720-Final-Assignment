from typing import Set, List, Callable
from model import Record
import crud_helpers as helper
import os
from server.util import working_directory
import util.binary_io as file_helper


def select(dbName:str, tableName: str, projectFieldNames:str, conditions: str) -> list[Record.Record]:
    wd = working_directory.load_working_directory()
    file_path = wd + '/' + dbName + '/' + tableName

    if os.path.exists(dbName+'/'+ tableName):
        #get file contents
        contents = file_helper.read_from_binary_file(file_path)
        contents_split = contents.split()
        field_names = contents.split()[0].split(' ') #get field names
        field_names_index = {}

        #create dict with index values for field names
        f_counter = 0
        for f in field_names:
            field_names_index[f] = f_counter
            f_counter = f_counter +1

        #get field names to be projected
        projections = projectFieldNames.split(',')
        

        #break down conditions
        conditions_list =  helper.create_conds_lst(conditions.split())

        #method to evaluate each record
        select_lst = [projections]
        
        for record in contents_split[1:]:
            projected_record = []
            result = helper.evaluate_conditions(conditions_list,record, field_names_index)
            if result:
                for p in projections:
                    projected_record = projected_record + [record[field_names_index[p]]] 
                select_lst = select_lst + [projected_record]
        
        #return select_lst

        # return_table = {record for record in contents_split if all(cond(record) for cond in conditions)}
        # return return_table 
    else:
        raise Exception("Table Does not Exist")  







def show_databases(working_directory: str) -> list[str]: 
  return os.listdir(working_directory)