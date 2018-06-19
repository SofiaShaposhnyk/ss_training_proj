from marshmallow import Schema, fields
from sanic.exceptions import SanicException


class ValidationError(SanicException):
    pass


class BaseForm(Schema):
    def handle_error(self, exc, data):
        raise ValidationError(exc, status_code=422)


class UsersSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    login = fields.String(required=True)
    password_hash = fields.String(required=True)


class ProjectsSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    user_id = fields.Integer()
    create_date = fields.Date()


class InvoicesSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    project_id = fields.Integer(required=True)
    description = fields.String()
