import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa
from config import db

metadata = sa.MetaData()

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
            await connection.execute('DROP DATABASE IF EXISTS ss_train')
            await connection.execute('CREATE DATABASE ss_train')
            await prepare_tables()
    await engine.wait_closed()


async def prepare_tables():
    async with create_engine('user={db_user} dbname={db_name} host={db_host} password={db_password}'.format(**db)) as engine:
        async with engine.acquire() as connection:
            await create_tables(connection)
            await upsert_entry(connection, users, login='user_111', password_hash='password_111')
            await upsert_entry(connection, users, login='login_2', password_hash='password_2')
            result = await get_all_entry(connection, users)
            print(result)
    await engine.wait_closed()


async def upsert_entry(conn, table_name, **kwargs):
    insert_query = table_name.insert().values(**kwargs)
    await conn.execute(insert_query)


async def delete_entry(conn, table_name, id_entry=None):
    delete_query = table_name.delete().where(table_name == id_entry)
    await conn.execute(delete_query)


async def get_all_entry(conn, table_name):
    return convert_resultproxy_to_list(await conn.execute(table_name.select()))


def convert_resultproxy_to_list(result_proxy):
    result = []
    for row in result_proxy:
        result.append(dict(row))
    return result


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
