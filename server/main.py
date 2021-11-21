from dotenv import load_dotenv
from model.Request import Request
from model.Privileges import Privileges
from model.ParsedQuery import ParsedQuery
from simple_websocket_server import WebSocketServer, WebSocket
from util.working_directory import load_working_directory, create_working_directory
from util import query_parser
import asyncio
import service.authentication_service
import os
import sqlvalidator
import ast
import service.crud.delete
import service.crud.update
import service.crud.create
import service.crud.read


working_directory = load_working_directory()

try:
  if os.path.exists(working_directory) == False:
    raise Exception("Working directory not found")
except:
  create_working_directory()


if os.path.exists("./.env"):
  load_dotenv("./.env")
else:
  load_dotenv("./dev.env")


lockingQueries: list[str] = []


async def lockingQueriesChecker():
  global lockingQueries
  currentQuery: str = lockingQueries[0]
  try:
    parsed_query = query_parser.parser(currentQuery)
    if str.upper(currentQuery[0]) == Privileges.INSERT.name:
      service.crud.insert.insert_record(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
    elif str.upper(currentQuery[0]) == Privileges.UPDATE.name:
      service.crud.update.update_records(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
    elif str.upper(currentQuery[0]) == Privileges.DELETE.name:
     service.crud.delete.delete_records(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.filters)
  except:
    pass
  lockingQueries = lockingQueries[1:]
  await asyncio.sleep(1)
  lockingQueriesChecker()

lockingQueriesChecker()


class WebSocketController(WebSocket):

    def handle(self):
        request: Request = ast.literal_eval(self.data)

        #TODO : first message from user should be an auth
        # try:
        #   request.token = service.authentication_service.authenticate_user(request)
        #   if type(request.username) == str or type(request.password):
        #     self.send_message(request.token)
        #     return
        # except:
        #   self.send_message('{"error": "Unauthorized access. Are you logged in?"}')
        #   return

        if sqlvalidator.parse(request.query) == False:
          self.send_message("Invalid sql query")
          return

        query = request.query.replace(";", "")
        splittedQuery = query.split(" ")

        if str.upper(splittedQuery[0]) == Privileges.INSERT.name or str.upper(splittedQuery[0]) == Privileges.UPDATE.name or str.upper(splittedQuery[0]) == Privileges.DELETE.name:
          lockingQueries.append(request.query)
          self.send_message('{"message": "Query appended to execution queue"}')
          return

        parsed_query: ParsedQuery = query_parser.parser(query)

        if splittedQuery[0] == Privileges.SHOW.name:
          if splittedQuery[1].upper() == "DATABASES":
            service.crud.read.show_databases(working_directory)
        elif splittedQuery[0] == Privileges.SELECT.name:
          service.crud.read.select_records(request.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
        elif splittedQuery[0] == Privileges.CREATE.name:
          if str.upper(splittedQuery[1]) == "DATABASE":
            service.crud.create.create_database(splittedQuery[2])
          if str.upper(splittedQuery[1]) == "TABLE":
            service.crud.create.create_table(request.database, parsed_query.table_name, parsed_query.selectors)
          if str.upper(splittedQuery[1]) == "INDEX":
            service.crud.create.create_table(splittedQuery[2], parsed_query.table_name, parsed_query.selectors)

        self.send_message("")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()
