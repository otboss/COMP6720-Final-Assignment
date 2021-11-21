from model.Record import Record
import os

def select_records(db_name:str, table_name: str, selectors: list[str] , filters: list[str]) -> list[Record]:
    pass

def show_databases(working_directory: str) -> list[str]: 
  return os.listdir(working_directory)