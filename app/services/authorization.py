import hashlib
import secrets
from sanic.response import json
from sanic.exceptions import Unauthorized
from app.domain.users import Users
from app.services.redis_connection import RedisConnection


available_url = ['/login', '/registration']


async def get_token():
    return secrets.token_hex(16)


async def check_login_data(login, password):

    hashed_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
    stored_info = await Users.get_by_login(login)
    stored_pass = stored_info[0]['password_hash']
    if hashed_pass == stored_pass:
        token = await get_token()
        await insert_redis(token, login)
        return await response_token(token)
    else:
        raise Unauthorized("Authorization error")


async def response_token(token):
    response = json({'message': 'authorized'},
                    headers={'Authorization': token},
                    status=200)
    return response


async def insert_redis(token, login):
    connection = await RedisConnection.get_connection()
    await connection.set(token, login, expire=86400)


async def check_token_in_redis(token):
    connection = await RedisConnection.get_connection()
    try:
        await connection.get(token)
        return token
    except TypeError:
        raise Unauthorized('Authorization error')


async def check_token(request):
    token = request.headers.get('Authorization')
    if request.path in available_url:
        return True
    elif token == await check_token_in_redis(token):
        return True
    else:
        raise Unauthorized('Authorization error')
