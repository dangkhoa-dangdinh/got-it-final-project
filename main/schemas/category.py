from marshmallow import fields

from main.schemas.base import BaseSchema, not_blank


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=not_blank)
    user_id = fields.Integer(dump_only=True)


class CategoryListSchema(BaseSchema):
    per_page = fields.Integer(required=True, dump_default=20)
    page = fields.Integer(required=True, dump_default=1)
    total = fields.Integer(required=True)
    items = fields.Nested(CategorySchema(), many=True)
