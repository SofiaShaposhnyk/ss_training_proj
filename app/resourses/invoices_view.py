from sanic.views import HTTPMethodView
from app.resourses.service_resource import invoice


class InvoicesView(HTTPMethodView):
    @staticmethod
    async def get(request, id_project):
        return await invoice(request, id_project)

    @staticmethod
    async def post(request, id_project):
        return await invoice(request, id_project)

    @staticmethod
    async def delete(request, id_project):
        return await invoice(request, id_project)
