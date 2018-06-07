import asynctest
from aiopg import sa
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from config import db
from app.models import Base, User
from app.database import get_all_entry


class TestDatabase(asynctest.TestCase):

    @staticmethod
    def create_sync_engine_test():
        return create_engine('postgresql://{user}:{password}@{host}/test'.format(**db))

    @staticmethod
    def create_sync_engine_post():
        return create_engine('postgresql://{user}:{password}@{host}/postgres'.format(**db))

    @classmethod
    def prepare_tables(cls):
        engine = cls.create_sync_engine_test()
        Base.metadata.create_all(engine)

    @staticmethod
    async def create_async_engine():
        return sa.create_engine('user={user} dbname=test host={host} password={password}'.format(**db))

    @classmethod
    def setUpClass(cls):
        engine = cls.create_sync_engine_post()
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT").execute('create database test')
            cls.prepare_tables()

    @classmethod
    def tearDownClass(cls):
        engine = cls.create_sync_engine_post()
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT").execute('drop database test')

    async def setUp(self):
        async with await self.create_async_engine() as engine:
            async with engine.acquire() as connection:
                insert_1 = insert(User).values(login='user_1', password='pass_hash_1')
                insert_2 = insert(User).values(login='user_2', password='pass_hash_2')
                await connection.execute(insert_1)
                await connection.execute(insert_2)

    async def test_get_entry_all(self):
        expected = [{'id': 1, 'login': 'user_1', 'password': 'pass_hash_1'},
                    {'id': 2, 'login': 'user_2', 'password': 'pass_hash_2'}]
        actual = await get_all_entry(User)
        self.assertEqual(expected, actual)
