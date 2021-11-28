from model.Block import Block
from model.Record import Record
import json
import copy


#A file is basically a table, one is created whenever a table is created
class File:

    #TODO: Update schema to be a list of Schema objects
    def __init__(self, table_name: str, schema: list[str]):
      self.data_items: list[Block] = []  # the list that will hold everything
      self.table_name = table_name
      self.schema = schema

    def add_block(self, block: Block):  # blocks is a list of records, where each record is a list
        for record in block.records:
            entry_keys = record.keys()
            if all(elem in self.schema for elem in entry_keys) == False:
              raise Exception("invalid block record provided, schema mismatch")

        # the file is created as a list of lists where the first list is the column headers
        self.data_items.append(block)

    @staticmethod
    def from_dict(file: dict):
      file_parsed = File(file["table_name"], file["schema"])
      for block in file["data_items"]:
        file_parsed.add_block(Block.from_dict(block))
      return file_parsed

    def to_dict(self) -> dict:
      file_dict = copy.copy(self.__dict__)

      def parse_block(block: Block):
        return block.__dict__
      file_dict["data_items"] = list(map(parse_block, file_dict["data_items"]))
      return file_dict
