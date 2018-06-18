from sanic.views import HTTPMethodView
from sanic.response import json
import datetime
from app.domain.projects import Projects
from app.services.acl_manager import set_delete_permissions, get_id_by_token


class ProjectsView(HTTPMethodView):
    @staticmethod
    async def get(request):
        user_id = await get_id_by_token(request)
        return json(await Projects.get_project(user_id))

    @staticmethod
    async def post(request):
        user_id = await get_id_by_token(request)
        await Projects.insert_project(user_id=user_id,
                                      create_date=datetime.date.today(),
                                      acl=await set_delete_permissions(request))
        return json({'message': 'entry created'})

    @staticmethod
    async def delete(request):
        await Projects.delete_project()
        return json({'message': 'projects deleted'})
