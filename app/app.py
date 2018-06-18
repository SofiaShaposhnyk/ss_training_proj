from sanic import Sanic
from app.services.engine import DBEngine
from app.resourses import login_view, registration_view, projects_view, \
    project_view, invoices_view, invoice_view
from app.services.redis_connection import RedisConnection
from app.services.authorization import check_token

app = Sanic(__name__)


@app.listener('after_server_stop')
async def close_db(app, loop):
    engine = await DBEngine.get_engine()
    engine.close()
    await engine.wait_closed()
    redis_conn = await RedisConnection.get_connection()
    redis_conn.close()


@app.middleware('request')
async def check_access(request):
    await check_token(request)


app.add_route(login_view.LoginView.as_view(), '/login')
app.add_route(registration_view.RegistrationView.as_view(), '/registration')
app.add_route(projects_view.ProjectsView.as_view(), '/projects')
app.add_route(project_view.ProjectView.as_view(), '/projects/<project_id>')
app.add_route(invoices_view.InvoicesView.as_view(), '/projects/<project_id>/invoices')
app.add_route(invoice_view.InvoiceView.as_view(), '/projects/<project_id>/invoices/<invoice_id>')
