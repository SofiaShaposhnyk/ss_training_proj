from sanic.views import HTTPMethodView
from sanic.response import json
from app.services.acl_manager import give_access, get_permissions, get_id_by_token, delete_access


class AccessView(HTTPMethodView):
    @staticmethod
    async def post(request):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, request.form.get('item_id')) in delete_access:
            await give_access(request.form.get('item_id'),
                              request.form.get('user_id'),
                              request.form.get('permissions'))
            return json({'message': 'permissions updated'})
        else:
            return json({'message': 'access denied'}, status=403)
