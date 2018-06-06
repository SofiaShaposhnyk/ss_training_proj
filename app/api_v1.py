from sanic import Blueprint
from app.service_resource import (smoke, project, login,
            add_session_to_request)


bp = Blueprint('api_v1')


bp.add_route(smoke, '/smoke', methods=['GET'])
bp.add_route(project, '/project', methods=['GET', 'POST', 'PUT', 'DELETE'])
bp.add_route(login, '/login', methods=['POST'])
