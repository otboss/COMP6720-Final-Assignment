# Service responsible for user authentication
from model.Credentials import Credentials
from model.Request import Request

def authenticate_user(request: Request) -> str:
    # TODO: Implement authentication, generate user access token (uuid). Hash and store token to database 
    # and use to authenticate all future queries from the user. Tokens are valid for 30 minutes

    if type(request.username) == str and type(request.password) == str:
        # TODO: Hash password using bcrypt and query database for user. Otherwise throw an error
        return "NEW ACCESS TOKEN"

    if type(request.token) == str:
        # TODO: Hash token and check if token exists in database. If the user is found
        # check if they have adequate permissions to execute the provided query. If so then
        # then return the  access token otherwise throw an error
        return request.token

    raise "unauthorized"