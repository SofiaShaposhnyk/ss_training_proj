import hashlib
import secrets
import asyncio_redis
from sanic.response import json
from sanic.exceptions import Unauthorized
from app import database as db


async def get_token():
    return secrets.token_hex(16)


async def check_login_data(request):
    user_info = {
        'login': request.args.get('login'), 'password': request.args.get('password').encode('utf-8')
    }
    hashed_pass = hashlib.md5(user_info['password']).hexdigest()
    stored_info = await db.get_user_by_login(request.args.get('login'))
    stored_pass = stored_info[0]['password_hash']
    if hashed_pass == stored_pass:
        token = await get_token()
        await insert_redis(user_info['login'], token)
        await write_cookie(token)
    else:
        return Unauthorized("Authorization error")


async def write_cookie(token):
    response = json({})
    response.cookies['token'] = token
    return response


async def insert_redis(login, token):
    connection = await asyncio_redis.Connection.create(host='localhost', port='6379', poolsize=10)
    await connection.set(login, token)
