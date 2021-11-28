from enum import Enum

class Request:
    username: str
    password: str
    token: str
    query: str
    database: str

    @staticmethod
    def from_json(request_json: dict):
        request = Request()
        request.username = request_json.get("username")
        request.password = request_json.get("password")
        request.token = request_json.get("token")
        request.query = request_json.get("query")
        request.database = request_json.get("database")
        return request
