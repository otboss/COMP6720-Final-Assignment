import Credentials
from server.model.Role import Role

# User : Structures user data
class User(Credentials):
  
  roles: list[Role] = []
  
  def __init__(self, username: str, password: str, roles: list[Role]):
    self.username = username
    self.password = password
    self.roles = roles