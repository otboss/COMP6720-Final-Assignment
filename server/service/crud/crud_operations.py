from typing import Set, List, Callable
from model import Record, Constants
import os
import util.binary_io as file_helper


#retrieves records from a table based on conditions given
# def select(table: Set[Record], conditions: List[Callable]) -> Set[Record]:
#     return_table = {record for record in table if all(cond(record) for cond in conditions)}
#     return return_table


def select(dbName:str, tableName: str, projectFieldNames:str, conditions: str) -> list[Record.Record]:
    if os.path.exists(dbName+'/'+ tableName):
        #get file contents
        contents = file_helper.read_from_binary_file(tableName)
        contents_split = contents.split()
        field_names = contents.split()[0].split(' ') #get field names
        field_names_index = {}

        #create dict with index values for field names
        f_counter = 0
        for f in field_names:
            field_names_index[f] = f_counter
            f_counter =+1

        


        #get field names to be projected
        projections = projectFieldNames.split(',')
        

        #break down conditions
        conditions_list =  create_conds_lst(conditions)

        #method to perform each condition
      


        return_table = {record for record in contents_split if all(cond(record) for cond in conditions)}
        return return_table 
    else:
        raise Exception("Table Does not Exist")  

#adds records to a table
#def insert(records: Set[Record], table_name: str) -> bool:
    #use table_name to locate the table file in the database folder then add the records to the file
    #return true or false indicating the success of the insert
    #b=4




def create_conds_lst(lst):
    conditions_lst = []
    conds_lst = []
    conds_index = 0
    sub_lst = []
    operator = ''
    length = len(lst) 
    count = 1
    for i in lst:
        if i in Constants.logical_operators:
            i_index = lst.index(i)
            conds_lst = lst[conds_index: i_index]
            #print(i)
            operator = i
            #print(conds_lst)
            sub_lst = lst[i_index +1:]
            #print(sub_lst)
            conditions_lst = [conds_lst] + [operator] + create_conds_lst(sub_lst)
            return conditions_lst 
        count = count +1
        if count == length:
            conditions_lst =  [lst]
    return conditions_lst



#updates specified values in records
def update( table_name: str,  conditions: List[Callable] ) -> bool:
    '''use table_name to locate the table file in the database folder then get all records and update records 
       where the conditions are met. Overwrite the file with new file containing the updates

       Return true or false indicating the success of the update
    '''
    c=3


#deletes specified records
def delete(table_name: str,  conditions: List[Callable] ) -> bool:
    '''use table_name to locate the table file in the database folder then get all records and delete records 
       where the conditions are met. Overwrite the file with new file without the deleted records

       Return true or false indicating the success of the update
    '''
    d=4

