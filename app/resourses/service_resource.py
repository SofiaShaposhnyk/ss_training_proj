from sanic.response import json, text
from marshmallow import ValidationError
from app.database import create_user, get_entry, delete_entry, insert_entry,\
    update_entry, projects, invoices
from app.services.authorization import check_login_data
from app.services.validation import ProjectsSchema, InvoicesSchema


async def login(request):
    await check_login_data(request)


async def registration(request):
    return await create_user(request)


async def project(request):
    if request.method == 'GET':
        return json(await get_entry(projects))
    if request.method == 'POST':
        json_data = request.args
        try:
            data = ProjectsSchema().load(json_data)
        except ValidationError:
            return json({'message': 'Invalid parameters'})
        await insert_entry(projects, user_id=data[0]['user_id'],
                           create_date=data[0]['create_date'])
    if request.method == 'DELETE':
        await delete_entry(projects)
        return text('projects deleted')


async def project_id(request, id_project):
    if request.method == 'GET':
        return json(await get_entry(projects, id_project))
    if request.method == 'PUT':
        json_data = request.args
        try:
            data = ProjectsSchema().load(json_data)
        except ValidationError:
            return json({'message': 'Invalid parameters'})
        await update_entry(projects, id_project, user_id=data[0]['user_id'],
                           create_date=data[0]['create_date'])
    if request.method == 'DELETE':
        await delete_entry(projects, id_project)
        return text('projects deleted')


async def invoice(request, id_project):
    if request.method == 'GET':
        return json(await get_entry(invoices, project_id=id_project))
    if request.method == 'POST':
        json_data = request.args
        try:
            data = InvoicesSchema().load(json_data)
        except ValidationError:
            return json({'message': 'Invalid parameters'})
        await insert_entry(invoices, project_id=data[0]['project_id'],
                           description=data[0]['description'])
    if request.method == 'DELETE':
        await delete_entry(invoices)
        return text('invoices deleted')


async def invoice_id(request, id_project, id_invoice):
    if request.method == 'GET':
        return json(await get_entry(invoices, id_project, id_invoice))
    if request.method == 'PUT':
        json_data = request.args
        try:
            data = InvoicesSchema().load(json_data)
        except ValidationError:
            return json({'message': 'Invalid parameters'})
        await update_entry(invoices, id_invoice, project_id=data[0]['project_id'],
                           description=data[0]['description'])
    if request.method == 'DELETE':
        await delete_entry(invoices, id_invoice)
        return text('invoices deleted')
