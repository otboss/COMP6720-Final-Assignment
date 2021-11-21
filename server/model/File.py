from model.Block import Block

#A file is basically a table, one is created whenever a table is created
class File:

    def __init__ (self, table_name: str, schema: list[str]):
      self.data_items: list[Block] = [] #the list that will hold everything
      self.table_name = table_name
      self.schema = schema
    
    def table_str(self, field_name: list[str]):
        col =[] #the list for column header
        for i in field_name:
            col.append(i)
        self.data_items.append(col)

    def add_block(self, block: Block): # blocks is a list of records, where each record is a list
        for records in block:
          for entry in records:
            entry_keys = dict.keys(entry)
            if all(elem in self.schema for elem in entry_keys) == False:
              raise Exception("invalid block record provided, schema mismatch")

        # the file is created as a list of lists where the first list is the column headers
        self.data_items.append(block)

def from_dict(file: dict) -> File:
  file_parsed = File(file["table_name"], file["schema"])
  for block in file.data_items:
    file_parsed.add_block(Block.from_dict(block))
  return file_parsed      