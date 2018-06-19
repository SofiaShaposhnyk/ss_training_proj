from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.invoices import Invoices
from app.services.validation import InvoicesSchema
from app.services.acl_manager import get_id_by_token, get_permissions, \
    delete_access, update_access, view_access


class InvoicesView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in view_access:
            return json(await Invoices.get_invoice(project_id=project_id))
        else:
            return json({'message': 'access denied'}, status=403)

    @staticmethod
    async def post(request, project_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in update_access:
            data = InvoicesSchema().load(request.form)
            await Invoices.insert_invoice(project_id=project_id,
                                          description=data[0]['description'])
            return json({'message': 'invoice created'})
        else:
            return json({'message': 'access denied'}, status=403)

    @staticmethod
    async def delete(request, project_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in delete_access:
            await Invoices.delete_invoice(project_id)
            return json({'message': 'invoices deleted'})
        else:
            return json({'message': 'access denied'}, status=403)
