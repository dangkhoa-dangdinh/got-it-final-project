from string import ascii_lowercase, ascii_uppercase, digits

from marshmallow import ValidationError, fields, post_load

from main.models.user import UserModel
from main.schemas.base import BaseSchema


def validate_password(password):
    if len(password) < 6:
        raise ValidationError("Passwords must have at least 6 characters")

    has_lower = False
    has_upper = False
    has_digit = False
    for char in password:
        if char in ascii_lowercase:
            has_lower = True
        elif char in ascii_uppercase:
            has_upper = True
        elif char in digits:
            has_digit = True

    if not (has_upper and has_lower and has_digit):
        raise ValidationError(
            "Password must include at least one "
            "lowercase letter, one uppercase letter, one digit"
        )


class UserSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate_password)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)
