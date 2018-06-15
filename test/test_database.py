import asynctest
import pytest
import asyncio
import sqlalchemy_utils
from aiopg.sa import create_engine
from app.config import db
from app.services.engine import create_db, create_tables


class TestDatabase(asynctest.TestCase):

    _engine = None

    @classmethod
    async def setup_engine(cls):
        if not cls._engine:
            cls._engine = await create_engine(user=db['db_user'],
                                              password=db['db_password'],
                                              host=db['db_host'],
                                              dbname='ss_test')

    @classmethod
    async def setup_database(cls):
        await create_db('ss_test')
        await cls.setup_engine()
        await create_tables(cls._engine)

    def setUpClass(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TestDatabase.setup_database())

    def tearDownClass(self):
        sqlalchemy_utils.drop_database('postgres://{db_user}:{db_password}@{db_host}/ss_test'.format(**db))
