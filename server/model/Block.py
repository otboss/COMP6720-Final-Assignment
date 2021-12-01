import copy

# Block : Stored by Files and used to store Records
class Block:
  records = []

  def __init__(self):
    self.records = []

  def add_record(self, record: dict):
    if(len(self.records) >= 5):
      raise Exception("block full") 

    self.records.append(record)

  @staticmethod
  def from_dict(block_dict: dict):
    block = Block()
    block.records = block_dict.get("records")
    return block

  def to_dict(self) -> dict:
    return copy.copy(self.__dict__)
    