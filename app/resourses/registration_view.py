from sanic.views import HTTPMethodView
from sanic.response import json
from app.domain.users import Users


class RegistrationView(HTTPMethodView):
    @staticmethod
    async def post(request):
        await Users.insert_user(request.form.get('login'),
                                request.form.get('password'))
        return json({'message': 'user created'})
