from sanic.response import json, text
from processor.authorization import tokenize

async def smoke(request):
    return text('hello, world!')


# TODO: get token via jwt
async def login(request):
    token = await tokenize({request.args.get('user'): request.args.get('pass')})
    return text(token)


# TODO: add functions for comunicate with DB
async def project(request):
    if request.method == 'GET':
        return text('this is project with GET')
    if request.method == 'POST':
        return text('this is project with POST')
    if request.method == 'PUT':
        return text('this is project with PUT')
    if request.method == 'DELETE':
        return text('this is project with DELETE')
