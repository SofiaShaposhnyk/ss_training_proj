from sanic.response import json, text
from processor.authorization import tokenize
from app.database import get_entry, delete_entry, insert_entry, update_entry, projects, invoices
from app.services.authorization import check_login_data


async def smoke(request):
    return text('hello, world!')


async def login(request):
    await check_login_data(request)


async def project(request):
    if request.method == 'GET':
        return json(await get_entry(projects))
    if request.method == 'POST':
        await insert_entry(projects, user_id=request.args.get('user_id'),
                           create_date=request.args.get('create_date'))
        return text('this is project with POST')
    if request.method == 'DELETE':
        await delete_entry(projects)
        return text('projects deleted')


async def project_id(request, id_project):
    if request.method == 'GET':
        return json(await get_entry(projects, id_project))
    if request.method == 'PUT':
        await update_entry(projects, id_project, user_id=request.args.get('user_id'),
                           create_date=request.args.get('create_date'))
        return text('this is project with PUT')
    if request.method == 'DELETE':
        await delete_entry(projects, id_project)
        return text('projects deleted')


async def invoice(request, id_project):
    if request.method == 'GET':
        return json(await get_entry(invoices, project_id=id_project))
    if request.method == 'POST':
        await insert_entry(invoices, project_id=request.args.get('project_id'),
                           description=request.args.get('description'))
        return text('this is invoice with POST')
    if request.method == 'DELETE':
        await delete_entry(invoices)
        return text('invoices deleted')


async def invoice_id(request, id_project, id_invoice):
    if request.method == 'GET':
        return json(await get_entry(invoices, id_project, id_invoice))
    if request.method == 'PUT':
        await update_entry(invoices, id_invoice, project_id=request.args.get('project_id'),
                           description=request.args.get('description'))
        return text('this is invoice with PUT')
    if request.method == 'DELETE':
        await delete_entry(invoices, id_invoice)
        return text('invoices deleted')
