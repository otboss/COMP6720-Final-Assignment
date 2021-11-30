from model.Block import Block
from model.Record import Record
from model.Schema import Schema
import json
import copy



# File : A file represents a table. It is instanciated upon table creation
class File:

    def __init__(self, table_name: str, schema: list[Schema]):
      self.data_items: list[Block] = []  # the list that will hold everything
      self.table_name = table_name
      self.schema = schema

    # Appends a block to the records attribute
    def add_block(self, block: Block):
        for record in block.records:
            entry_keys = record.keys()
            if all(elem in self.schema for elem in entry_keys) == False:
              raise Exception("invalid block record provided, schema mismatch")

        # the file is created as a list of lists where the first list is the column headers
        self.data_items.append(block)

    # Converts a dictonary representing a File object into a File object
    @staticmethod
    def from_dict(file: dict):
      file_parsed = File(file["table_name"], file["schema"])
      for block in file["data_items"]:
        file_parsed.add_block(Block.from_dict(block))
      return file_parsed

    # Converts a File object to a dictionary
    def to_dict(self) -> dict:
      file_dict = copy.copy(self.__dict__)
      def parse_block(block: Block):
        return block.__dict__
      file_dict["data_items"] = list(map(parse_block, file_dict["data_items"]))
      return file_dict
