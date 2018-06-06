import asynctest
from aiopg import sa
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from database.config import db
from database.models import Base, User
from database.helpers import get_entry


class TestDatabase(asynctest.TestCase):

    @staticmethod
    def create_sync_engine(name):
        return create_engine('postgresql://{user}:{password}@{host}/{name}'.format(name=name, **db))

    @staticmethod
    async def create_async_engine():
        return sa.create_engine('user={user} dbname=test host={host} password={password}'.format(**db))

    @classmethod
    def setUpClass(cls):
        engine = create_engine('postgres')
        with engine:
            with engine.connect() as connection:
                connection.execute('create database test')
        Base.metadata.create_all(create_engine('test'))

    @classmethod
    def tearDownClass(cls):
        engine = create_engine('postgres')
        with engine:
            with engine.connect() as connection:
                connection.execute('drop database test')

    async def setUp(self):
        engine = await self.create_async_engine()
        async with engine:
            async with engine.acqure() as connection:
                insert_1 = insert(User).values(login='user_1', password='pass_hash_1')
                insert_2 = insert(User).values(login='user_2', password='pass_hash_2')
                connection.execute(insert_1)
                connection.execute(insert_1)

    async def test_get_entry_all(self):
        expected = [{'id': 1, 'login': 'user_1', 'password': 'pass_hash_1'},
                    {'id': 2, 'login': 'user_2', 'password': 'pass_hash_2'}]
        actual = await get_entry(User)
        self.assertEqual(expected, actual)
