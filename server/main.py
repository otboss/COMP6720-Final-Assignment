from typing import List
from dotenv import load_dotenv
from model.Request import Request
from service import authentication_service
from simple_websocket_server import WebSocketServer, WebSocket
import os
import sqlvalidator
import ast

if os.path.exists("./.env"):
  load_dotenv("./.env")
else:
  load_dotenv("./dev.env")


queryQueue: List = []

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

        if str.upper(splittedQuery[0]) == "INSERT" or str.upper(splittedQuery[0]) == "UPDATE" or str.upper(splittedQuery[0]) == "DELETE":
          queryQueue.append(request.query)
      


        # TODO: Handle sql query
        self.send_message("")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

print("started websocket server on port: "+os.environ.get("PORT"))
server = WebSocketServer('', os.environ.get("PORT"), WebSocketController)
server.serve_forever()