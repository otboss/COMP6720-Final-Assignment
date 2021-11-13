from typing import List
from dotenv import load_dotenv
from model.Request import Request
from server.model.Privileges import Privileges
from simple_websocket_server import WebSocketServer, WebSocket
import asyncio
import service.database_service
import service.authentication_service
import os
import sqlvalidator
import ast
from threading import Timer




if os.path.exists("./.env"):
  load_dotenv("./.env")
else:
  load_dotenv("./dev.env")


lockingQueries: list[str] = []

async def lockingQueriesChecker():
  global lockingQueries
  currentQuery: str = lockingQueries[0]
  try:
    # TODO: execute query
    pass
  except:
    pass
  lockingQueries = lockingQueries[1:]
  await asyncio.sleep(1)
  lockingQueriesChecker()

lockingQueriesChecker()


class WebSocketController(WebSocket):

    def handle(self):
        #TODO : first message from user should be an auth        
        request: Request = ast.literal_eval(self.data)

        try:
          request.token = service.authentication_service.authenticate_user(request)
          if type(request.username) == str or type(request.password):
            self.send_message(request.token)
            return
        except:
          self.send_message("Unauthorized access. Are you logged in?")
          return

        if sqlvalidator.parse(request.query) == False:
          self.send_message("Invalid sql query")
          return

        splittedQuery = request.query.replace(";", "").split(" ")

        if str.upper(splittedQuery[0]) == Privileges.INSERT.name or str.upper(splittedQuery[0]) == Privileges.UPDATE.name or str.upper(splittedQuery[0]) == Privileges.DELETE.name:
          lockingQueries.append(request.query)
          self.send_message("Query appended to execution queue")
          return

        # TODO: Handle non locking sql query
        if splittedQuery[0] == Privileges.SHOW.name:
          if splittedQuery[1].upper() == "DATABASES":
            # TODO: PROVIDE WORKING DIRECTORY TO SERVICE BELOW
            service.databases_service.show_databases("TODO: PROVIDE WORKING DIRECTORY HERE")
            
        self.send_message("")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()