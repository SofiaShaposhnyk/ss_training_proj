from sanic.views import HTTPMethodView
from app.resourses.service_resource import project_id


class ProjectView(HTTPMethodView):
    @staticmethod
    async def get(request, id_project):
        return await project_id(request, id_project)

    @staticmethod
    async def put(request, id_project):
        return await project_id(request, id_project)

    @staticmethod
    async def delete(request, id_project):
        return await project_id(request, id_project)

