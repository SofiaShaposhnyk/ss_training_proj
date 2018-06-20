from test.crud_test import TestCRUD
from app.domain.invoices import Invoices


class TestInvoices(TestCRUD):

    def test_get_invoice(self):
        actual = self.loop.run_until_complete(Invoices.get_invoice(3, 6))
        expected = ({'id': 6, 'project_id': 3, 'description': ' description_6'},)
        self.assertEqual(actual, expected)

    def test_get_invoices(self):
        actual = self.loop.run_until_complete(Invoices.get_invoice(2))
        expected = ({'id': 4, 'project_id': 2, 'description': ' description_4'},
                    {'id': 5, 'project_id': 2, 'description': ' description_5'})
        self.assertEqual(expected, actual)

    def test_update_invoice(self):
        expected = ({'id': 7, 'project_id': 4, 'description': 'description_777'},)
        self.loop.run_until_complete(Invoices.update_invoice(4, 7, description='description_777'))
        actual = self.loop.run_until_complete(Invoices.get_invoice(4, 7))
        self.assertEqual(actual, expected)

    def test_delete_invoice(self):
        expected = ()
        self.loop.run_until_complete(Invoices.delete_invoice(5, 10))
        actual = self.loop.run_until_complete(Invoices.get_invoice(5, 10))
        self.assertEqual(expected, actual)

#    def test_insert_invoice(self):
#        expected = ({'id': 11, 'project_id': 4, 'description': 'description_11'},)
#        self.loop.run_until_complete(Invoices.insert_invoice(4, description='description_11'))
#        actual = self.loop.run_until_complete(Invoices.get_invoice(4, 11))
#        self.assertEqual(expected, actual)
