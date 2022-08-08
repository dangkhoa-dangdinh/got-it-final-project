from flask import jsonify
from marshmallow import RAISE, Schema, fields, pre_load, validate


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

    @pre_load
    def strip_whitespace(self, data, **__):
        return {
            key.strip(): value.strip()
            for key, value in data.items()
            if isinstance(key, str) and isinstance(value, str)
        }


class PaginationSchema(BaseSchema):
    # If user input per_page > 20 -> raise Error
    per_page_range_validator = validate.Range(1, 20)

    per_page = fields.Integer(load_default=20, validate=per_page_range_validator)
    page = fields.Integer(load_default=1)
    total = fields.Integer(dump_only=True)
