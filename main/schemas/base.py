from flask import jsonify
from marshmallow import RAISE, Schema, fields, validate


class BaseSchema(Schema):
    length_validator = validate.And(
        validate.Length(min=1, error="Fields cannot be blank"),
        validate.Length(max=256, error="Maximum length of fields is 256"),
    )

    class Meta:
        # For unknown input fields, raise ValidationError
        unknown = RAISE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    # If user input per_page > 20 -> raise Error
    per_page_range_validator = validate.Range(1, 20)

    per_page = fields.Integer(
        required=True, dump_default=20, validate=per_page_range_validator
    )
    page = fields.Integer(required=True, dump_default=1)
    total = fields.Integer(dump_only=True)
