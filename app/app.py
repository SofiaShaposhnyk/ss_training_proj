from sanic import Sanic
from sanic.views import HTTPMethodView
from app.database import DBEngine
from app.web_part.service_resource import smoke, project, login, invoice, project_id, invoice_id

app = Sanic(__name__)


class SmokeView(HTTPMethodView):
    @staticmethod
    async def get(request):
        return await smoke(request)


class LoginView(HTTPMethodView):
    @staticmethod
    async def post(request):
        return await login(request)


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


class InvoiceView(HTTPMethodView):
    @staticmethod
    async def get(request, id_invoice, id_project):
        return await invoice_id(request, id_invoice, id_project)

    @staticmethod
    async def put(request, id_project, id_invoice):
        return await invoice_id(request, id_invoice, id_project)

    @staticmethod
    async def delete(request, id_invoice, id_project):
        return await invoice_id(request, id_invoice, id_project)


@app.listener('after_server_stop')
async def close_db(app, loop):
    engine = await DBEngine.get_connection()
    engine.close()
    await engine.wait_closed()


app.add_route(SmokeView.as_view(), '/smoke')
app.add_route(LoginView.as_view(), '/login')
app.add_route(ProjectsView.as_view(), '/projects')
app.add_route(ProjectView.as_view(), '/projects/<id_project>')
app.add_route(InvoicesView.as_view(), '/projects/<id_project>/invoices')
app.add_route(InvoiceView.as_view(), '/projects/<id_project>/invoices/<id_invoice>')
