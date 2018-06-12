from sanic import Sanic
from app.database import DBEngine
from app.resourses import login_view, registration_view, projects_view, \
    project_view, invoices_view, invoice_view

app = Sanic(__name__)


@app.listener('after_server_stop')
async def close_db(app, loop):
    engine = await DBEngine.get_engine()
    engine.close()
    await engine.wait_closed()


app.add_route(login_view.LoginView.as_view(), '/login')
app.add_route(registration_view.RegistrationView.as_view(), '/registration')
app.add_route(projects_view.ProjectsView.as_view(), '/projects')
app.add_route(project_view.ProjectView.as_view(), '/projects/<id_project>')
app.add_route(invoices_view.InvoicesView.as_view(), '/projects/<id_project>/invoices')
app.add_route(invoice_view.InvoiceView.as_view(), '/projects/<id_project>/invoices/<id_invoice>')
