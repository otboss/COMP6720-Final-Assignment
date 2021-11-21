from model.Record import  Record

class Block:
  records = []

  def add_record(self, record: Record):
    if(len(self.records) >= 5):
      raise Exception("block full") 

    self.records.append(record.to_list())

def from_dict(block_dict: dict) -> Block:
  block = Block()
  for record in block_dict:
    block.add_record(Record.from_dict(record))
  return block
    