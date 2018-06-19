from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.projects import Projects
from app.services.validation import ProjectsSchema
from app.services.acl_manager import get_id_by_token, get_permissions, \
    update_access, delete_access


class ProjectView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id):
        user_id = await get_id_by_token(request)
        return json(await Projects.get_project(user_id, project_id))

    @staticmethod
    async def put(request, project_id):
        data = ProjectsSchema().load(request.form)
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in update_access:
            await Projects.update_project(project_id,
                                          create_date=data[0]['create_date'])
            return json({'message': 'project updated'})
        else:
            return json({'message': 'access denied'}, status=403)

    @staticmethod
    async def delete(request, project_id):
        user_id = await get_id_by_token(request)
        if await get_permissions(user_id, project_id) in delete_access:
            await Projects.delete_project(user_id, project_id)
            return json({'message': 'project deleted'})
        else:
            return json({'message': 'access denied'}, status=403)
