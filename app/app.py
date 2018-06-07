from sanic import Sanic
from sanic.views import HTTPMethodView
from web_part.service_resource import (smoke, project, login)

app = Sanic(__name__)

class SmokeView(HTTPMethodView):
    async def get(self, request):
        return await smoke(request)


class ProjectView(HTTPMethodView):
    async def get(self, request):
        return await project(request)

    async def post(self, request):
        return await project(request)

    async def put(self, request):
        return await project(request)

    async def delete(self, request):
        return await project(request)


class LoginView(HTTPMethodView):
    async def post(self, request):
        return await login(request)
    

app.add_route(SmokeView.as_view(), '/smoke')
app.add_route(ProjectView.as_view(), '/projects')
app.add_route(LoginView.as_view(), '/login')
