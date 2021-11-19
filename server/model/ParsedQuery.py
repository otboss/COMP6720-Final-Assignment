from model.Privileges import Privileges


class ParsedQuery:

  database: str = None
  table_name: str = None
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
  def update(table_name: str, selectors: list[str], filters: list[str] = []):
    query = ParsedQuery
    query.operation = Privileges.UPDATE
    query.table_name = table_name
    query.selectors = selectors
    query.filters = filters
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
  def create(database: str, table_name: str = None):
    query = ParsedQuery
    query.operation = Privileges.CREATE
    query.database = database
    query.table_name = table_name
    return query

  @staticmethod
  def drop(database: str, table_name: str = None):
    query = ParsedQuery
    query.operation = Privileges.DROP
    query.database = database
    query.table_name = table_name
    return query
