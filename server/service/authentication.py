from model.Credentials import Credentials
from exception.AuthenticationError import AuthenticationError

AccessToken = str

def create_access_token(credentials: Credentials) -> AccessToken:
    # TODO: Hash password using bcrypt and query database for user. Otherwise throw an error
    raise AuthenticationError("invalid credentials")

def verify_access_token(access_token: AccessToken) -> bool:
    # TODO: Hash token and check if token exists in database. If the user is found
    # check if they have adequate permissions to execute the provided query. If so then
    # then return the  access token otherwise throw an error
    pass