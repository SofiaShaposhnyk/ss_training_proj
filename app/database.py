from aiopg.sa import create_engine
import sqlalchemy as sa
from config import db

metadata = sa.MetaData()


class DBEngine(object):
    __engine = None
    __connection = None

    @staticmethod
    async def get_connection():
        if not DBEngine.__connection:
            await DBEngine.set_state()
        return DBEngine.__connection

    @staticmethod
    async def set_state():
        DBEngine.__engine = await create_engine(user=db['db_user'],
                                                password=db['db_password'],
                                                host=db['db_host'],
                                                dbname=db['db_name'])
        DBEngine.__connection = await DBEngine.__engine.acquire()


users = sa.Table('users', metadata,
                 sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
                 sa.Column('login', sa.String(255), nullable=False),
                 sa.Column('password_hash', sa.String(255), nullable=False))

projects = sa.Table('projects', metadata,
                    sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
                    sa.Column('user_id', None, sa.ForeignKey('users.id')),
                    sa.Column('create_date', sa.Date, nullable=False))

invoices = sa.Table('invoices', metadata,
                    sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
                    sa.Column('project_id', None, sa.ForeignKey('projects.id')),
                    sa.Column('description', sa.String(255)))


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


async def create_db():
    async with create_engine('user={db_user} host={db_host} password={db_password}'.format(**db)) as engine:
        async with engine.acquire() as connection:
            await connection.execute('DROP DATABASE IF EXISTS {}'.format(db['db_name']))
            await connection.execute('CREATE DATABASE {}'.format(db['db_name']))
            await prepare_tables()
    await engine.wait_closed()


async def prepare_tables():
            await create_tables(await DBEngine.get_connection())


async def insert_entry(table_name, **kwargs):
        conn = await DBEngine.get_connection()
        insert_query = table_name.insert().values(**kwargs)
        await conn.execute(insert_query)


async def update_entry(table_name, req_id, **kwargs):
        conn = await DBEngine.get_connection()
        update_query = table_name.update().where(table_name.columns.id == req_id).values(**kwargs)
        await conn.execute(update_query)


async def delete_entry(table_name, entry_id=None):
        conn = await DBEngine.get_connection()
        delete_query = table_name.delete().where(table_name.columns.id == int(entry_id))
        await conn.execute(delete_query)


# NEED REFACTOR
async def get_entry(table_name, entry_id=None, project_id=None):
        conn = await DBEngine.get_connection()
        if entry_id:
            if project_id:
                return convert_resultproxy_to_list(await conn.execute(table_name.select(
                    table_name.columns.id == entry_id and table_name.columns.project_id == project_id)))
            else:
                return convert_resultproxy_to_list(await conn.execute(
                    table_name.select(table_name.columns.id == entry_id)))
        else:
            if project_id:
                return convert_resultproxy_to_list(await conn.execute(table_name.select().where(
                    table_name.columns.project_id == project_id)))
            else:
                return convert_resultproxy_to_list(await conn.execute(table_name.select()))


def convert_resultproxy_to_list(result_proxy):
    result = []
    for row in result_proxy:
        result.append(dict(row))
    return result
