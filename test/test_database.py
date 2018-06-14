import asynctest
import asyncio
from aiopg.sa import create_engine
from app.config import db
from app.services.engine import create_db


class TestDatabase(asynctest.TestCase):

    class TestEngine(object):
        __engine = None

        @classmethod
        async def get_engine(cls):
            if not cls.__engine:
                cls.__engine = await create_engine(user=db['db_user'],
                                                   password=db['db_password'],
                                                   host=db['db_host'],
                                                   dbname=db['test_db'])
            return cls.__engine

    @classmethod
    def setUpClass(cls):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_db('test_db'))

    @classmethod
    def tearDownClass(cls):
        loop = asyncio.get_event_loop()
        engine = loop.run_until_complete(cls.TestEngine.get_engine())
        with loop.run_until_complete(engine.acquire()) as connection:
            connection.execute('drop database test_db')

    async def test_test(self):
        self.assertEqual(25, 25)
