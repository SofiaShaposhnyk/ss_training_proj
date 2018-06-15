from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.invoices import Invoices
from app.services.validation import InvoicesSchema


class InvoiceView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id, invoice_id):
        return json(await Invoices.get_invoice(project_id, invoice_id))

    @staticmethod
    async def put(request, project_id, invoice_id):
        data = InvoicesSchema().load(request.form)
        await Invoices.update_invoice(project_id, invoice_id, description=data[0]['description'])
        return json({'message': 'invoice updated'})

    @staticmethod
    async def delete(request, project_id, invoice_id):
        await Invoices.delete_invoice(project_id, invoice_id)
        return json({'message': 'invoices deleted'})
