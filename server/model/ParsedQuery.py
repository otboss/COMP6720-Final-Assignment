from model.Privileges import Privileges

# ParsedQuery : Structures the components of a query after it has been parsed
class ParsedQuery:
  database: str = None
  table_name: str = None
  index: str = None
  values: list[str] = []
  operation: Privileges = None
  selectors: list[str] = []
  filters: list[str] = []
  
  @staticmethod
  def select(table_name: str, selectors: list[str], filters: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.SELECT
    query.table_name = table_name
    query.selectors = selectors
    query.filters = filters
    return query

  @staticmethod
  def update(table_name: str, selectors: list[str], values: list[str], filters: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.UPDATE
    query.table_name = table_name
    query.selectors = selectors
    query.filters = filters
    query.values = values
    return query

  @staticmethod
  def insert(table_name: str, selectors: list[str], filters: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.INSERT
    query.table_name = table_name
    query.selectors = selectors
    query.filters = filters
    return query

  @staticmethod
  def delete(table_name: str, filters: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.DELETE
    query.table_name = table_name
    query.filters = filters
    return query

  @staticmethod
  def create_database(database: str):
    query = ParsedQuery
    query.operation = Privileges.CREATE
    query.database = database
    return query

  @staticmethod
  def create_table(table_name: str, selectors: list[str] = ["id"]):
    query = ParsedQuery
    query.operation = Privileges.CREATE
    query.table_name = table_name
    query.selectors = selectors
    return query  

  @staticmethod
  def create_index(index: str, table_name: str, selectors: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.CREATE
    query.index = index
    query.table_name = table_name
    query.selectors = selectors
    return query

  @staticmethod
  def drop(database: str, table_name: str = None):
    query = ParsedQuery
    query.operation = Privileges.DROP
    query.database = database
    query.table_name = table_name
    return query

  @staticmethod
  def describe(table_name: str):
    query = ParsedQuery
    query.operation = Privileges.DESCRIBE
    query.table_name = table_name
    return query
