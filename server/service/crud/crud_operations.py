from typing import Set, List, Callable
from model import Record
import crud_helpers as helper
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

#adds records to a table
#def insert(records: Set[Record], table_name: str) -> bool:
    #use table_name to locate the table file in the database folder then add the records to the file
    #return true or false indicating the success of the insert
    #b=4




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

