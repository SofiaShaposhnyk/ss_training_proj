from sanic.views import HTTPMethodView
from app.services.acl_manager import give_access


class AccessView(HTTPMethodView):
    @staticmethod
    async def post(request):
        return await give_access(request.form.get('item_id'),
                                 request.form.get('user_id'),
                                 request.form.get('permissions'))
