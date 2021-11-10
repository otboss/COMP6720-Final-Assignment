

class Record:
  
  def __init__(self, id: int, param1: str, param2: str):
    self.id = id
    self.param1 = param1
    self.param2 = param2

  def to_list(self):
    return [
      self.id,
      self.param1,
      self.param2,      
    ]