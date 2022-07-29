from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()


def validate_password(password):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$"
    validator = validate.Regexp(
        reg,
        error="Passwords must have at least 6 characters, including at least one "
        "lowercase letter, one uppercase letter, one digit",
    )
    return validator(password)


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    hashed_password = fields.String()
    salt = fields.String()


class CategorySchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String()


class ItemSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    description = fields.String()
