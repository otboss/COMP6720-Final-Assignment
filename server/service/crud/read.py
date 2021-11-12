from model.Record import Record
import os

def select_records(db_name:str, table_name: str, project_field_names:str , conditions: str) -> list[Record]:
    if os.path.exists(table_name):
        #get file contents
        contents = file_helper.read_from_binary_file(table_name)
        contents_split = contents.split()
        field_names = contents.split()[0].split(' ') #get field names
        

        #get field names to be projected
        projections = project_field_names.split(',')
        projections_index = {}

        p_counter = 0
        for p in projections:
            projections_index.ke
            p_counter = p_counter +1


        return_table = {record for record in contents_split if all(cond(record) for cond in conditions)}
        return return_table 
    else:
        raise Exception("Table Does not Exist")

def show_databases(working_directory: str) -> list[str]: 
  return os.listdir(working_directory)