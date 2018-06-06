from aiopg.sa import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from database.config import db
from database import models

dsn = 'user={user} dbname={db_name} host={host} ' \
      'password={password}'.format(**db)


async def create_db_engine():
    engine = await create_engine(dsn)
    return engine


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


async def upsert_entry(table_name, **kwargs):
    engine = await create_db_engine()
    async with engine:
        async with engine.acquire() as connection:
            insert_query = insert(table_name).values(**kwargs)
            if table_name == models.User:
                insert_query = insert_query.on_conflict_do_update(
                    index_elements=['login'], set_=kwargs)
            await connection.execute(insert_query)


async def get_entry(table_name, id=None):
    engine = await create_db_engine()
    async with engine:
        async with engine.acquire() as connection:
            if id:
                select_query = select([table_name]).where(table_name.id == id)
            else:
                select_query = select([table_name])
            result = await connection.execute(select_query)
            return _convert_resultproxy_to_list(result)
