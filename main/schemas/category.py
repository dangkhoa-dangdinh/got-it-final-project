from marshmallow import fields

from main.commons.exceptions import BadRequest, ValidationError
from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    user_id = fields.Integer(dump_only=True)

    def handle_error(
        self, error: ValidationError, data: [id, name, user_id], *, many: bool, **kwargs
    ):
        raise BadRequest()
