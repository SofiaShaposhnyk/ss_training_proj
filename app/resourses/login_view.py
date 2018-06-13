from sanic.views import HTTPMethodView
from app.services.authorization import check_login_data


class LoginView(HTTPMethodView):
    @staticmethod
    async def post(request):
        return await check_login_data(request.form.get('login'),
                                      request.form.get('password'))
