from marshmallow import Schema, fields, ValidationError


class BaseForm(Schema):
    def handle_error(self, exc, data):
        raise ValidationError(exc, status_code=422)


class UsersSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    login = fields.String(required=True)
    password_hash = fields.String(required=True)


class ProjectsSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    user_id = fields.Integer(required=True)
    create_date = fields.Date(required=True)


class InvoicesSchema(BaseForm):
    id = fields.Integer(dump_only=True, required=True)
    project_id = fields.Integer(required=True)
    description = fields.String()
