from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, validate

not_blank = validate.Length(min=1, error="Fields cannot be blank")


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    per_page = fields.Integer(required=True, dump_default=20)
    page = fields.Integer(required=True, dump_default=1)
    total = fields.Integer()
