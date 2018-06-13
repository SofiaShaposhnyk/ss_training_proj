import hashlib
from app.database import DBEngine
from app.services.models import users


class Users(object):

    @staticmethod
    async def create(login, password):
        pass_hash = hashlib.md5(password.encode('utf-8'))
        await insert_entry(users, login=request.args.get('login'),
                           password_hash=pass_hash.hexdigest())

    @staticmethod
    async def get_by_login(req_login):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(users.select(users.columns.login == req_login))
            return convert_resultproxy_to_list(result)

    @staticmethod
    async def insert(login, password_hash):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(users.insert().values(login=login, password_hash=password_hash))
