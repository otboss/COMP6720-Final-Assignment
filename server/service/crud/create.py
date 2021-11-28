from model.File import File
from model.Block import Block
from model.Record import Record
from util import binary_io
from util.binary_io import write_to_binary_file, append_to_binary_file
import util.working_directory
import os
import json

def create_database(database_name: str):
    try:
        util.working_directory.create_sub_folder(database_name)
    except:
        pass

def create_table(database: str, table_name: str, field_names: list[str]):#field_names is a list
    working_dir = util.working_directory.load_working_directory()
    table_path = "%s/%s/%s"%(working_dir, database, table_name)
    if os.path.exists(table_path):
        raise Exception("Table already exists")
    else:
        new_table= File(table_name, field_names)
        new_table_json = json.dumps(new_table.to_dict())
        write_to_binary_file(table_path, new_table_json)

def insert_record (database: str, table_name: str, record: str):
    working_dir = util.working_directory.load_working_directory()
    table_path = "%s/%s/%s"%(working_dir, database, table_name)
    if os.path.exists("%s.bin"%(table_path)):
        contents: File = File.from_dict(json.loads(binary_io.read_from_binary_file(table_path)))
        record_for_insert: Record = Record(contents.schema, eval("[%s]"%(record)))
        if len(contents.data_items) > 0:
            last_block: Block = contents.data_items[-1]
            contents.data_items[-1] = last_block
            binary_io.write_to_binary_file(table_path, contents.to_dict())
        else:
            new_block = Block()
            new_block.add_record(record_for_insert)
            contents.data_items.append(new_block)
            binary_io.write_to_binary_file(table_path, json.dumps(contents.to_dict()))
    else:
        raise Exception("Table Does not Exist")

def create_index(database: str, table_name: str, index: str):
    pass