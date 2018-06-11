import datetime
import jwt
from sanic.response import text
from app import database as db


KEY = 'secret'
ALGORITHM = 'HS256'


async def get_token():
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
    return jwt.encode({'exp': exp_time}, KEY, ALGORITHM)


async def check_login_data(request):
    user_info = {
        request.args.get('login'): request.args.get('password')
    }
    hashed_info = jwt.encode(user_info, KEY, ALGORITHM)
    stored_info = await db.get_user_by_login(request.args.get('login'))
    if hashed_info == stored_info:
        return text("true")
