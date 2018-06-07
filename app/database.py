from aiopg.sa import create_engine
import sqlalchemy
# import asyncio
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db
from app import models

dsn = 'user={user} dbname={db_name} host={host} password={password}'.format(**db)
dsn_default = 'user={user} host={host} password={password}'.format(**db)


async def create_db_engine():
    return await create_engine(dsn)


async def create_default_engine():
    return await create_engine(dsn_default)


async def create_db():
    with await create_default_engine() as engine:
        with await engine.acquire() as connection:
            connection.execute('CREATE DATABASE IF NOT EXIST {}'.format(db['db_name']))
    await engine.wait_closed()


def prepare_tables():
    engine = sqlalchemy.create_engine('postgresql://{user}:{password}@{host}/{db_name}'.format(**db))
    models.Base.metadata.creale_all(engine)


def _convert_resultproxy_to_list(result_proxy) -> list:
    '''
    Convert ResultProxy object to list of dictionaries.
    :param ResultProxy result_proxy: ResultProxy object to convert
    :return list: list of dictionaries
    '''
    dict_result = []
    for row in result_proxy:
        dict_result.append(dict(row))
    return dict_result


async def delete_entry(table, id) -> None:
    table = table.__table__
    async with await create_db_engine() as engine:
        async with engine.acquire() as connection:
            delete = table.delete().where(table.id == id)
            await connection.execute(delete)
    engine.wait_closed()


async def upsert_entry(table_name, **kwargs):
    async with await create_db_engine() as engine:
        async with engine.acquire() as connection:
            insert_query = insert(table_name).values(**kwargs)
            if table_name == models.User:
                insert_query = insert_query.on_conflict_do_update(
                    index_elements=['login'], set_=kwargs)
            await connection.execute(insert_query)
    engine.wait_closed()


async def get_entry(table_name, id=None):
    async with await create_db_engine() as engine:
        async with engine.acquire() as connection:
            if id:
                select_query = select([table_name]).where(table_name.id == id)
            else:
                select_query = select([table_name])
            result = await connection.execute(select_query)
    engine.wait_closed()
    return _convert_resultproxy_to_list(result)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(create_db())
# prepare_tables()
