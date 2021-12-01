import json

# Credentials : Used to structure user credentials
class Credentials:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def from_dict(credentials: dict):
        return Credentials(credentials["username"], credentials["password"])
