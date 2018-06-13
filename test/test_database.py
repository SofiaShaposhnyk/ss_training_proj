import asynctest
from aiopg import sa
from sqlalchemy.dialects.postgresql import insert
from app.config import db
from app.database import get_entry, create_db, users, projects, invoices


class TestDatabase(asynctest.TestCase):

    class TestEngine(object):
        __engine = None

        @staticmethod
        async def get_engine():
            if not TestDatabase.TestEngine.__engine:
                await TestDatabase.TestEngine.set_state()
            return TestDatabase.TestEngine.__engine

        @staticmethod
        async def set_state():
            TestDatabase.TestEngine.__engine = \
                await sa.create_engine(user=db['db_user'],
                                       password=db['db_password'],
                                       host=db['db_host'],
                                       dbname='test_db')

    @classmethod
    async def setUpClass(cls):
        await create_db('test_db')

    @classmethod
    async def tearDownClass(cls):
        engine = await cls.TestEngine.get_engine()
        with engine.acquire() as connection:
            connection.execute('drop database test_db')

    async def test_get_entry_all(self):
        expected = [{'id': 1, 'login': 'user_1', 'password': 'pass_hash_1'},
                    {'id': 2, 'login': 'user_2', 'password': 'pass_hash_2'}]
        actual = await get_entry(users)
        self.assertEqual(expected, actual)
