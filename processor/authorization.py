import jwt
from os import environ

KEY = 'secret'# environ.get('KEY')
ALGORITHM = 'HS256'

# TODO: add storage and expiration time for tokens
async def tokenize(login_data):
    token = jwt.encode(login_data, KEY, ALGORITHM)
    return token
