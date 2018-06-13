from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.invoices import Invoices
from app.services.validation import InvoicesSchema


class InvoicesView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id):
        return json(await Invoices.get(project_id=project_id))

    @staticmethod
    async def post(request, project_id):
        data = InvoicesSchema().load(request.form)
        await Invoices.insert(project_id=project_id,
                              description=data[0]['description'])
        return json({'message': 'invoice created'})

    @staticmethod
    async def delete(request, project_id):
        await Invoices.delete(project_id)
        return json({'message': 'invoices deleted'})
