from model.Privileges import Privileges


class ParsedQuery:
  database: str = None
  table_name: str = None
  index: str = None
  operation: Privileges = None
  selectors: list[str] = []
  filters: list[str] = []

def select(table_name: str, selectors: list[str], filters: list[str] = []) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.SELECT
  query.table_name = table_name
  query.selectors = selectors
  query.filters = filters
  return query

def update(table_name: str, selectors: list[str], filters: list[str] = []) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.UPDATE
  query.table_name = table_name
  query.selectors = selectors
  query.filters = filters
  return query

def insert(table_name: str, selectors: list[str], filters: list[str] = []) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.INSERT
  query.table_name = table_name
  query.selectors = selectors
  query.filters = filters
  return query

def delete(table_name: str, filters: list[str] = []) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.DELETE
  query.table_name = table_name
  query.filters = filters
  return query

def create_database(database: str) -> ParsedQuery:
  query = ParsedQuery
  query.database = database
  return query

def create_table(table_name: str, selectors: list[str] = ["id"]) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.CREATE
  query.table_name = table_name
  query.selectors = selectors
  return query  

def create_index(index: str, table_name: str, selectors: list[str] = []) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.CREATE
  query.index = index
  query.table_name = table_name
  query.selectors = selectors
  return query

def drop(database: str, table_name: str = None) -> ParsedQuery:
  query = ParsedQuery
  query.operation = Privileges.DROP
  query.database = database
  query.table_name = table_name
  return query
