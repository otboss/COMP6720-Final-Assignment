from enum import Enum

class Request:
    username: str
    password: str
    token: str
    query: str
    action: str


class Actions(Enum):
    EXECUTE = 1,
    COMMIT = 2,