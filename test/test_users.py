import asyncio
import unittest
import sqlalchemy_utils
from app.services.engine import DBEngine
from app.config import db
from app.services.engine import create_db, create_tables
from test.insert_into_db import insert_users_data, \
    insert_projects_data, insert_invoices_data, delete_all_from_db
from app.domain.users import Users
from test.crud_test import TestCRUD


class TestUsers(TestCRUD):

#    def test_get_hash_by_login(self):
#        expected = 'be718d4d359ac7531e991f99952dd475'
#        actual = self.loop.run_until_complete(Users.get_hash_by_login('user_2'))
#        self.assertEqual(actual, expected)

#    def test_get_id_by_login(self):
#        expected = 1
#        actual = self.loop.run_until_complete(Users.get_id_by_login('user_1'))
#        self.assertEqual(actual, expected)

    def test_get_user(self):
        expected = ({'id': 1, 'login': ' user_1', 'password_hash': ' fc5889dcfb42598c8b3ddc543fabca43'},)
        actual = self.loop.run_until_complete(Users.get_user(1))
        self.assertEqual(expected, actual)

    def test_get_user_none(self):
        expected = ()
        actual = self.loop.run_until_complete(Users.get_user(5))
        self.assertEqual(actual, expected)

#    def test_insert_user(self):
#        login = 'user_4'
#        password = 'password_4'
#        expected = ({'id': 4, 'login': ' user_4', 'password_hash': ' 213542493168006f524332b422b53dd0'},)
#        self.loop.run_until_complete(Users.insert_user(login, password))
#        actual = self.loop.run_until_complete(Users.get_user(4))
#        self.assertEqual(expected, actual)
