from dotenv import load_dotenv
from model.Request import Request
from model.Privileges import Privileges
from model.ParsedQuery import ParsedQuery
from model.Query import Query
from util import binary_io
from simple_websocket_server import WebSocketServer, WebSocket
from util.working_directory import load_working_directory, create_working_directory
from util import query_parser
from math import trunc
import asyncio
import service.authentication_service
import os
import sqlvalidator
import ast
import service.crud.delete
import service.crud.update
import service.crud.create
import service.crud.read
import datetime


working_directory = ""
try:
  working_directory = load_working_directory()
except:
  create_working_directory()
  working_directory = load_working_directory()


if os.path.exists("./.env"):
  load_dotenv("./.env")
else:
  load_dotenv("./dev.env")


lockingQueries: list[Query] = []


async def lockingQueriesChecker():
  global lockingQueries
  currentQuery: Query = lockingQueries[0]
  try:
    parsed_query = query_parser.parser(currentQuery.query)
    working_dir = load_working_directory()
    table_lock_file = "%s/%s/.%s-lock"%(working_dir, currentQuery.database, parsed_query.table_name)
    timestamp: int = trunc(datetime.datetime.now().timestamp()*1000)
    binary_io.write_to_binary_file(table_lock_file, str(timestamp))
    if str.upper(currentQuery[0]) == Privileges.INSERT.name:
      service.crud.update.insert_records(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
    elif str.upper(currentQuery[0]) == Privileges.UPDATE.name:
      service.crud.update.update_records(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
    elif str.upper(currentQuery[0]) == Privileges.DELETE.name:
      service.crud.delete.delete_records(working_directory, parsed_query.database, parsed_query.table_name, parsed_query.filters)
    binary_io.delete_binary_file(table_lock_file)
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

        if splittedQuery[0].upper() == Privileges.INSERT.name or splittedQuery[0].upper() == Privileges.UPDATE.name or splittedQuery[0].upper() == Privileges.DELETE.name:
          lockingQueries.append(Query(request.database, request.query))
          self.send_message('{"message": "Query is being processed"}')
          return

        parsed_query: ParsedQuery = query_parser.parser(query)

        if splittedQuery[0] == Privileges.SHOW.name:
          if splittedQuery[1].upper() == "DATABASES":
            service.crud.read.show_databases(working_directory)
        elif splittedQuery[0] == Privileges.SELECT.name:
          service.crud.read.select_records(request.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
        elif splittedQuery[0] == Privileges.CREATE.name:
          if splittedQuery[1].upper() == "DATABASE":
            service.crud.create.create_database(splittedQuery[2])
          if splittedQuery[1].upper() == "TABLE":
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
