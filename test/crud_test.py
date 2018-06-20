import unittest
import sqlalchemy_utils
import asyncio
from app.services.engine import create_tables, create_db, DBEngine
from app.config import db
from test.insert_into_db import insert_users_data, \
    insert_invoices_data, insert_projects_data, delete_all_from_db


class TestCRUD(unittest.TestCase):

    loop = None

    @classmethod
    async def setup_database(cls):
        await create_db()
        await create_tables(await DBEngine.get_engine())

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.setup_database())

    @classmethod
    def tearDownClass(cls):
        sqlalchemy_utils.drop_database('postgres://{db_user}:{db_password}@{db_host}/{db_name}'.format(**db))

    def setUp(self):
        insert_users_data()
        insert_projects_data()
        insert_invoices_data()

    def tearDown(self):
        delete_all_from_db()
