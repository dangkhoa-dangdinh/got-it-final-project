from marshmallow import fields

from main.schemas.base import BaseSchema, PaginationSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=BaseSchema.length_validator)
    description = fields.String(required=True, validate=BaseSchema.length_validator)
    category_id = fields.Integer(dump_only=True)


class ItemUpdateSchema(BaseSchema):
    name = fields.String(validate=BaseSchema.length_validator)
    description = fields.String(validate=BaseSchema.length_validator)


class ItemListSchema(PaginationSchema):
    items = fields.Nested(ItemSchema(), many=True)
