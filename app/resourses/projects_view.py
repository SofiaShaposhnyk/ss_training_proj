from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.projects import Projects
from app.services.validation import ProjectsSchema


class ProjectsView(HTTPMethodView):
    @staticmethod
    async def get(request):
        return json(await Projects.get())

    @staticmethod
    async def post(request):
        data = ProjectsSchema().load(request.form)
        await Projects.insert(user_id=data[0]['user_id'], create_date=data[0]['create_date'])
        return json({'message': 'entry created'})

    @staticmethod
    async def delete(request):
        await Projects.delete()
        return json({'message': 'projects deleted'})
