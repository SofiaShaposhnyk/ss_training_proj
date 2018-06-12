from sanic.views import HTTPMethodView
from app.resourses.service_resource import login


class LoginView(HTTPMethodView):
    @staticmethod
    async def post(request):
        return await login(request)
