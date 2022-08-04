from functools import wraps

from flask import request
from marshmallow import ValidationError as MarshmallowValidationError

from main.commons.exceptions import (
    CategoryNotFound,
    ForbiddenNotOwner,
    ItemNotFound,
    LackingAccessToken,
    UserNotFound,
    ValidationError,
)
from main.libs.utils import decode_jwt_token
from main.models.user import UserModel


def jwt_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            raise LackingAccessToken()
        try:
            payload = decode_jwt_token(token)
            user = UserModel.find_by(id=payload)
        except ValueError:
            raise UserNotFound()
        return func(user_id=user.id, *args, **kwargs)

    return decorator


def validate_input(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            method = request.method
            if method in ["POST", "PUT"]:
                data = request.get_json()
            else:
                data = request.args
            try:
                data = schema().load(data)
            except MarshmallowValidationError as error:
                raise ValidationError(error_data=error.messages)
            return func(data=data, *args, **kwargs)

        return wrapper

    return decorator


def check_existing_category(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _id = kwargs.get("category_id")
            category = model.find_by(id=_id)
            if not category:
                raise CategoryNotFound()
            return func(category=category, *args, **kwargs)

        return wrapper

    return decorator


def check_existing_item(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _id = kwargs.get("item_id")
            item = model.find_by(id=_id)
            if not item or kwargs.get("category").id != item.category_id:
                raise ItemNotFound()
            return func(item=item, *args, **kwargs)

        return wrapper

    return decorator


def check_owner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("category").user_id != kwargs.get("user_id"):
            raise ForbiddenNotOwner()
        return func(*args, **kwargs)

    return wrapper
