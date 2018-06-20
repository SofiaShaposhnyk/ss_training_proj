import datetime
from test.crud_test import TestCRUD
from app.domain.projects import Projects


class TestProjects(TestCRUD):

    def test_get_project(self):
        actual = self.loop.run_until_complete(Projects.get_project(1, 2))
        expected = ({'id': 2, 'user_id': 1, 'create_date': datetime.date(2017, 12, 1),
                     "acl": {"1": "DELETE", "2": "VIEW"}},)
        self.assertEqual(actual, expected)

    def test_get_projects(self):
        actual = self.loop.run_until_complete(Projects.get_project(3))
        expected = ({'id': 1, 'user_id': 1, 'create_date': datetime.date(2010, 10, 10),
                     "acl": {"1": "DELETE", "2": "UPDATE", "3": "VIEW"}},
                    {'id': 3, 'user_id': 2, 'create_date': datetime.date(2016, 5, 30),
                     "acl": {"2": "DELETE", "3": "VIEW"}},
                    {'id': 6, 'user_id': 3, 'create_date': datetime.date(2018, 4, 30),
                     "acl": {"3": "DELETE", "2": "VIEW"}})
        self.assertEqual(expected, actual)

    def test_update_project(self):
        expected = ({"id": 5, "user_id": 2, "create_date": datetime.date(2018, 10, 11), "acl": {"2": "DELETE"}},)
        self.loop.run_until_complete(Projects.update_project(5, create_date="2018-10-11"))
        actual = self.loop.run_until_complete(Projects.get_project(2, 5))
        self.assertEqual(actual, expected)

#    def test_insert_project(self):
#        expected = ({"id": 7, "user_id": 3, "create_date": datetime.date(2018, 6, 20), "acl": {"3": "DELETE"}},)
#        self.loop.run_until_complete(Projects.insert_project(3, '2018-06-17', {"3": "DELETE"}))
#        actual = self.loop.run_until_complete(Projects.get_project(3, 7))
#        self.assertEqual(expected, actual)


