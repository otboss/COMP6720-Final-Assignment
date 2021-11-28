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
import service.authentication_service
import os
import sqlvalidator
import service.crud.delete
import service.crud.update
import service.crud.create
import service.crud.read
import datetime
import json
import time
from threading import Thread

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

def lockingQueriesChecker():
  global lockingQueries
  while True:
    try:
      current_query: Query = lockingQueries[0]
      parsed_query = query_parser.parser(current_query.query)
      working_dir = load_working_directory()
      table_lock_file = "%s/%s/.%s-lock"%(working_dir, current_query.database, parsed_query.table_name)
      timestamp: int = trunc(datetime.datetime.now().timestamp()*1000)
      binary_io.write_to_binary_file(table_lock_file, str(timestamp))
      if parsed_query.operation == Privileges.INSERT:
        service.crud.create.insert_record(current_query.database, parsed_query.table_name, parsed_query.selectors)
      elif parsed_query.operation == Privileges.UPDATE:
        service.crud.update.update_records(current_query.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)
      elif parsed_query.operation == Privileges.DELETE:
        service.crud.delete.delete_records(current_query.database, parsed_query.table_name, parsed_query.filters)
      binary_io.delete_binary_file(table_lock_file)
    except Exception as e:
      if str(e) != "list index out of range":
        print(e)
    lockingQueries = lockingQueries[1:]
    time.sleep(1)

lockingQueriesCheckerThread = Thread(target=lockingQueriesChecker)
lockingQueriesCheckerThread.start()

class WebSocketController(WebSocket):

    def handle(self):
        try:
          request: Request = Request.from_json(json.loads(self.data))

          if request.username != None:
            self.send_message("")
            return

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
            query_obj = Query(request.database, request.query)
            lockingQueries.append(query_obj)
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
            if splittedQuery[1].upper() == "INDEX":
              service.crud.create.create_index(splittedQuery[2], parsed_query.table_name, parsed_query.selectors)
          self.send_message('{"message": "Query is being processed"}')
        except Exception as e:
          self.send_message('{"error": %s, "message": "Query could not be processed"}'%(e))

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()
