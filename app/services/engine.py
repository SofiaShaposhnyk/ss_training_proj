from aiopg.sa import create_engine
from app.config import db


class DBEngine(object):
    __engine = None

    @classmethod
    async def get_engine(cls):
        if not cls.__engine:
            cls.__engine = await create_engine(user=db['db_user'],
                                               password=db['db_password'],
                                               host=db['db_host'],
                                               dbname=db['db_name'])
        return cls.__engine


async def create_tables(engine):
    async with engine.acquire() as conn:
        await conn.execute('''CREATE TABLE users (
                                                  id serial PRIMARY KEY,
                                                  login varchar(255),
                                                  password_hash varchar(255))''')
        await conn.execute('''CREATE TABLE projects (
                                                     id serial PRIMARY KEY,
                                                     user_id int references users(id),
                                                     create_date date)''')
        await conn.execute('''CREATE TABLE invoices (
                                                     id serial PRIMARY KEY,
                                                     project_id int references projects(id),
                                                     description varchar(255))''')


async def create_db(db_name):
    async with create_engine('user={db_user} '
                             'host={db_host} '
                             'password={db_password}'.format(**db)) as engine:
        async with engine.acquire() as connection:
            await connection.execute('CREATE DATABASE {}'.format(db_name))
    await engine.wait_closed()


async def prepare_tables():
    await create_tables(await DBEngine.get_engine())


async def convert_resultproxy(result_proxy):
    return tuple(map(lambda row: dict(row), result_proxy))
