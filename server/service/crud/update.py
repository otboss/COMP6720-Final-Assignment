from model.File import File
from model.Record import Record
import util.binary_io
import json


def update_records(working_directory: str, database: str, table_name: str, selectors: str, filters: list[str]):
  '''use table_name to locate the table file in the database folder then get all records and update records 
      where the conditions are met. Overwrite the file with new file containing the updates

      Return true or false indicating the success of the update
  '''  

  table_path = "%s/%s/%s"%(working_directory, database, table_name)

  table_contents: str = util.binary_io.read_from_binary_file(table_path)

  table_contents_parsed: File = File.from_dict(json.loads(table_contents))


  # TODO: implement logic to process query and update table contents
  
  util.binary_io.write_to_binary_file(table_path, json.dumps(table_contents_parsed.to_dict))

  pass


def alter_table():
  # Ignore this functionality for now
  pass
