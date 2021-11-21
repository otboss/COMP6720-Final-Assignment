
class Record:

  def __init__(self, id: int, param1: str, param2: str):
    self.id = id
    self.param1 = param1
    self.param2 = param2
  
def from_dict(record: dict) -> Record:
  return Record(record["id"], record["param1"], record["param2"])
