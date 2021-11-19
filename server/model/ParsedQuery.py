from server.model.Privileges import Privileges


class ParsedQuery:

  database: str = None
  table_name: str = None
  operation: Privileges = None
  selectors: list[str] = []
  filters: list[str] = []

  @staticmethod
  def select(self, table_name: str, selectors: list[str], filters: list[str]):
    self.operation = Privileges.SELECT
    self.table_name = table_name
    self.selectors = selectors
    self.filters = filters
    return self

  @staticmethod
  def update(self, table_name: str, selectors: list[str], filters: list[str]):
    self.operation = Privileges.UPDATE
    self.table_name = table_name
    self.selectors = selectors
    self.filters = filters
    return self

  @staticmethod
  def insert(self, table_name: str, selectors: list[str], filters: list[str]):
    self.operation = Privileges.INSERT
    self.table_name = table_name
    self.selectors = selectors
    self.filters = filters
    return self
    
  @staticmethod
  def delete(self, table_name: str, filters: list[str]):
    self.operation = Privileges.DELETE
    self.table_name = table_name
    self.filters = filters
    return self
  
  @staticmethod
  def create(self, database: str, table_name: str):
    self.operation = Privileges.CREATE
    self.database = database
    self.table_name = table_name
    return self

  @staticmethod
  def drop(self, database: str, table_name: str = None):
    self.operation = Privileges.DROP
    self.database = database
    self.table_name = table_name
    return self
