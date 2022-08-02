from marshmallow import fields

from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    name = fields.String(required=True)
