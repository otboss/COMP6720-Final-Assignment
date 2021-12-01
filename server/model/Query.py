
# Query : Structures the required data needed to execute a query
class Query:

  def __init__(self, database: str, query: str):
    self.database = database
    self.query = query