from marshmallow import fields

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
