from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.invoices import Invoices
from app.services.validation import InvoicesSchema
from app.services.acl_manager import get_id_by_token, get_permissions, \
    view_access, update_access, delete_access


class InvoiceView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id, invoice_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in view_access:
            return json(await Invoices.get_invoice(project_id, invoice_id))
        else:
            return json({'message': 'access denied'}, status=403)

    @staticmethod
    async def put(request, project_id, invoice_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in update_access:
            data = InvoicesSchema().load(request.form)
            await Invoices.update_invoice(project_id, invoice_id,
                                          description=data[0]['description'])
            return json({'message': 'invoice updated'})
        else:
            return json({'message': 'access denied'}, status=403)

    @staticmethod
    async def delete(request, project_id, invoice_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in delete_access:
            await Invoices.delete_invoice(project_id, invoice_id)
            return json({'message': 'invoices deleted'})
        else:
            return json({'message': 'access denied'}, status=403)
