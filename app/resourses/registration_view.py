from sanic.views import HTTPMethodView
from app.resourses.service_resource import registration


class RegistrationView(HTTPMethodView):
    @staticmethod
    async def post(request):
        return await registration(request)
