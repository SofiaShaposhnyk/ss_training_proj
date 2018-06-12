import hashlib
import secrets
import asyncio_redis
from sanic.response import json
from sanic.exceptions import Unauthorized
from app import database as db


available_url = ['/login', '/registration']


async def get_token():
    return secrets.token_hex(16)


async def check_login_data(request):
    user_info = {
        'login': request.args.get('login'),
        'password': request.args.get('password').encode('utf-8')
    }
    hashed_pass = hashlib.md5(user_info['password']).hexdigest()
    stored_info = await db.get_user_by_login(request.args.get('login'))
    stored_pass = stored_info[0]['password_hash']
    if hashed_pass == stored_pass:
        token = await get_token()
        await insert_redis(token, user_info['login'])
        return await response_token(token)
    else:
        raise Unauthorized("Authorization error")


async def response_token(token):
    response = json({'message': 'authorized'},
                    headers={'authorization': token},
                    status=200)
    return response


async def insert_redis(token, login):
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    await connection.set(token, login, expire=86400)
    connection.close()


async def check_token_in_redis(token):
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    try:
        await connection.get(token)
    except TypeError:
        raise Unauthorized('Authorization error')
    else:
        return token


async def check_token(request):
    token = request.headers.get('authorization')
    if request.path in available_url:
        return True
    elif token == await check_token_in_redis(token):
        return True
    else:
        raise Unauthorized('Authorization error')
