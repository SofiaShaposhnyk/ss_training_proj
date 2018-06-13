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


async def create_tables(conn):
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
            await prepare_tables()
    await engine.wait_closed()


async def prepare_tables():
    await create_tables(await DBEngine.get_engine())


async def insert_entry(table_name, **kwargs):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as conn:
        insert_query = table_name.insert().values(**kwargs)
        await conn.execute(insert_query)


async def update_entry(table_name, req_id, **kwargs):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as conn:
        update_query = table_name.update().where(
            table_name.columns.id == req_id).values(**kwargs)
        await conn.execute(update_query)


async def delete_entry(table_name, entry_id=None):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as conn:
        delete_query = table_name.delete().where(
            table_name.columns.id == int(entry_id))
        await conn.execute(delete_query)


# NEEDS REFACTORING
async def get_entry(table_name, entry_id=None, project_id=None):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as conn:
        if entry_id:
            if project_id:
                return convert_resultproxy(await conn.execute(table_name.select(
                    table_name.columns.id == entry_id and
                    table_name.columns.project_id == project_id)))
            else:
                return convert_resultproxy(await conn.execute(
                    table_name.select(table_name.columns.id == entry_id)))
        else:
            if project_id:
                return convert_resultproxy(await conn.execute(table_name.select().where(
                    table_name.columns.project_id == project_id)))
            else:
                return convert_resultproxy(await conn.execute(table_name.select()))


def convert_resultproxy(result_proxy):
    return tuple(map(lambda row: dict(row), result_proxy))
