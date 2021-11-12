import shutil
import os

def drop_database(working_directory: str, database: str):
  if(working_directory[-1] != "/"):
    working_directory = working_directory + "/"
  shutil.rmtree(working_directory + database)

def drop_table(working_directory: str, database: str, table_name: str):
  if(working_directory[-1] != "/"):
    working_directory = working_directory + "/"
  os.remove(working_directory + database + "/" + table_name + ".bin")

def delete_records(condition: str):
  '''use table_name to locate the table file in the database folder then get all records and delete records 
      where the conditions are met. Overwrite the file with new file without the deleted records

      Return true or false indicating the success of the update
  '''  
  pass