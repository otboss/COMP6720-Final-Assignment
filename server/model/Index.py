import copy

# Index : Represents the structure for field indices of tables
class Index:

  def __init__(self, index_name: str, columns: list[str], values: dict[str, list[str]] = {}):
    self.index_name = index_name
    self.columns = columns
    self.values = values

  def to_dict(self):
    return copy.copy(self.__dict__)