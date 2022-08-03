from marshmallow import fields

from main.commons.exceptions import BadRequest, ValidationError
from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    category_id = fields.Integer(dump_only=True)

    def handle_error(
        self,
        error: ValidationError,
        data: [id, name, description, category_id],
        *,
        many: bool,
        **kwargs
    ):
        raise BadRequest()
