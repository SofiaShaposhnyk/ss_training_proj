from sanic.views import HTTPMethodView
from app.resourses.service_resource import project


class ProjectsView(HTTPMethodView):
    @staticmethod
    async def get(request):
        return await project(request)

    @staticmethod
    async def post(request):
        return await project(request)

    @staticmethod
    async def delete(request):
        return await project(request)
