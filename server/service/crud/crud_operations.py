from typing import Set, List, Callable

from model.Record import Record

#retrieves records from a table based on conditions given
def select(table: Set[Record], conditions: List[Callable]) -> Set[Record]:
    return_table = {record for record in table if all(cond(record) for cond in conditions)}
    return return_table

#adds records to a table
def insert(records: Set[Record], table_name: str) -> bool:
    #use table_name to locate the table file in the database folder then add the records to the file
    #return true or false indicating the success of the insert
    b=4

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

