from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.projects import Projects
from app.services.validation import ProjectsSchema


class ProjectView(HTTPMethodView):
    @staticmethod
    async def get(request, project_id):
        return json(await Projects.get(project_id))

    @staticmethod
    async def put(request, project_id):
        data = ProjectsSchema().load(request.form)
        await Projects.update(project_id, user_id=data[0]['user_id'],
                              create_date=data[0]['create_date'])
        return json({'message': 'project updated'})

    @staticmethod
    async def delete(request, id_project):
        await Projects.delete(id_project)
        return json({'message': 'project deleted'})
