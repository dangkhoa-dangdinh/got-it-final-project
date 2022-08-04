from marshmallow import fields

from main.schemas.base import BaseSchema, not_blank


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=not_blank)
    description = fields.String(required=True, validate=not_blank)
    category_id = fields.Integer(dump_only=True, required=True)


class ItemUpdateSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(allow_none=False)
    description = fields.String(allow_none=False)
    category_id = fields.Integer(dump_only=True)


class ItemListSchema(BaseSchema):
    per_page = fields.Integer(required=True, dump_default=20)
    page = fields.Integer(required=True, dump_default=1)
    total = fields.Integer(required=True)
    items = fields.Nested(ItemSchema(), many=True)
