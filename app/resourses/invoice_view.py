from sanic.views import HTTPMethodView
from app.resourses.service_resource import invoice_id


class InvoiceView(HTTPMethodView):
    @staticmethod
    async def get(request, id_invoice, id_project):
        return await invoice_id(request, id_invoice, id_project)

    @staticmethod
    async def put(request, id_project, id_invoice):
        return await invoice_id(request, id_invoice, id_project)

    @staticmethod
    async def delete(request, id_invoice, id_project):
        return await invoice_id(request, id_invoice, id_project)
