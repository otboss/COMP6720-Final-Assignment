from typing import List
from dotenv import load_dotenv
from model.Request import Request
from server.model.Privileges import Privileges
from service import authentication_service
from simple_websocket_server import WebSocketServer, WebSocket
import util.set_interval
import os
import sqlvalidator
import ast

if os.path.exists("./.env"):
  load_dotenv("./.env")
else:
  load_dotenv("./dev.env")


lockingQueries: list[str] = []

def lockingQueriesChecker():
  global lockingQueries
  currentQuery: str = lockingQueries[0]
  # TODO: execute query 
  lockingQueries = lockingQueries[1:]

util.set_interval.SetInterval(1.0, lockingQueriesChecker)


class WebSocketController(WebSocket):

    def handle(self):
        #TODO : first message from user should be an auth        
        request: Request = ast.literal_eval(self.data)

        try:
          request.token = authentication_service.authenticate_user(request)
          if type(request.username) == str or type(request.password):
            self.send_message(request.token)
            return
        except:
          self.send_message("Unauthorized access. Are you logged in?")
          return

        if sqlvalidator.parse(request.query) == False:
          self.send_message("Invalid sql query")
          return

        splittedQuery = request.query.split(" ")

        if str.upper(splittedQuery[0]) == Privileges.INSERT.name or str.upper(splittedQuery[0]) == Privileges.UPDATE.name or str.upper(splittedQuery[0]) == Privileges.DELETE.name:
          lockingQueries.append(request.query)
          self.send_message("Query appended to execution queue")
          return
      
        # TODO: Handle non locking sql query
        self.send_message("")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()