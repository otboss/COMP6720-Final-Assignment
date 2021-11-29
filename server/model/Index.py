class Index:
  def __init__(self, index_name: str, columns: list[str], ids: list):
    self.index_name = index_name
    self.columns = columns
    self.values: dict = {}