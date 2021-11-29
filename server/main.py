from dotenv import load_dotenv
from model.Request import Request
from model.Privileges import Privileges
from model.ParsedQuery import ParsedQuery
from model.Query import Query
from exception.InvalidQueryError import InvalidQueryError
from util import binary_io
from simple_websocket_server import WebSocketServer, WebSocket
from util.working_directory import load_working_directory, create_working_directory
from util import query_parser
from math import trunc
from threading import Thread
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


locking_queries: list[Query] = []

def locking_queriesChecker():
  global locking_queries
  while True:
    try:
      current_query: Query = locking_queries[0]
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
    locking_queries = locking_queries[1:]
    time.sleep(1)

locking_queriesCheckerThread = Thread(target=locking_queriesChecker)
locking_queriesCheckerThread.start()

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
            raise InvalidQueryError("invalid sql query provided")

          query = request.query.replace(";", "")
          splitted_query = query.split(" ")

          if splitted_query[0].upper() == Privileges.INSERT.name or splitted_query[0].upper() == Privileges.UPDATE.name or splitted_query[0].upper() == Privileges.DELETE.name:
            query_obj = Query(request.database, request.query)
            locking_queries.append(query_obj)
            return

          parsed_query: ParsedQuery = query_parser.parser(query)
          message = "Query is being processed"

          if splitted_query[0].upper() == Privileges.SHOW.name:
            if splitted_query[1].upper() == "DATABASES":
              self.send_message(json.dumps(service.crud.read.show_databases()))
              return
          elif splitted_query[0].upper() == Privileges.SELECT.name:
            self.send_message(json.dumps(service.crud.read.select_records(request.database, parsed_query.table_name, parsed_query.selectors, parsed_query.filters)))
            return
          elif splitted_query[0].upper() == Privileges.DESCRIBE.name:
            self.send_message(json.dumps(service.crud.read.describe_table(request.database, parsed_query.table_name)))
            return
          elif splitted_query[0].upper() == Privileges.CREATE.name:
            if splitted_query[1].upper() == "DATABASE":
              service.crud.create.create_database(splitted_query[2])
              message = "Database %s created"%(splitted_query[2])
            if splitted_query[1].upper() == "TABLE":
              service.crud.create.create_table(request.database, parsed_query.table_name, parsed_query.selectors)
              message = "Table %s created"%(parsed_query.table_name)
            if splitted_query[1].upper() == "INDEX":
              service.crud.create.create_index(splitted_query[2], parsed_query.table_name, parsed_query.selectors)
              message = "Index %s created"%(splitted_query[2])
          elif splitted_query[0] == Privileges.DROP.name:
            if splitted_query[1].upper() == "DATABASE":
              service.crud.delete.drop_database(splitted_query[2])
              message = "Database %s dropped"%(splitted_query[2])
            if splitted_query[1].upper() == "TABLE":
              service.crud.delete.drop_table(request.database, parsed_query.table_name, parsed_query.selectors)
              message = "Table '%s' dropped"%(parsed_query.table_name)
          
          self.send_message('{"message": "%s"}'%(message))
          
        except Exception as e:
          print("Error: ", str(e))
          self.send_message('{"error": "%s", "message": "Query could not be processed"}'%(e))

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()
