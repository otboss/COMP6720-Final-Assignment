from model.FieldTypes import FieldTypes


class Schema:
  
  def __init__(self, field: str, type: FieldTypes):
    self.field = field
    self.type = type