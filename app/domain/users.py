import hashlib
from app.services.engine import DBEngine, convert_resultproxy
from app.services.models import users


class Users(object):

    @staticmethod
    async def get_by_login(req_login):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            query = users.select(users.c.login == req_login)
            result = await conn.execute(query)
            return await convert_resultproxy(result)

    @staticmethod
    async def insert_user(login, password):
        pass_hash = hashlib.md5(password.encode('utf-8'))
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(users.insert().values(login=login,
                                                     password_hash=pass_hash.hexdigest()))

    @staticmethod
    async def delete_user(entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                delete_query = users.delete().where(users.columns.id == int(entry_id))
            else:
                delete_query = users.delete()
            await conn.execute(delete_query)

    @staticmethod
    async def get_user(entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                get_query = users.select(users.c.id == entry_id)
            else:
                get_query = users.select()
            return await convert_resultproxy(await conn.execute(get_query))
