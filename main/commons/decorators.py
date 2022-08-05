from functools import wraps

from flask import request
from marshmallow import ValidationError as MarshmallowValidationError

from main.commons.exceptions import (
    CategoryNotFound,
    ForbiddenNotOwner,
    ItemNotFound,
    LackingAccessToken,
    ValidationError,
)
from main.libs.utils import decode_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def jwt_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            raise LackingAccessToken()
        payload = decode_jwt_token(token)
        user = UserModel.find_by(id=payload)
        return func(user_id=user.id, *args, **kwargs)

    return decorator


def validate_input(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            http_method = request.method
            if http_method in ("POST", "PUT"):
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


def check_existing_category():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            category_id = kwargs.get("category_id")
            category = CategoryModel.find_by(id=category_id)
            if not category:
                raise CategoryNotFound()
            return func(category=category, *args, **kwargs)

        return wrapper

    return decorator


def check_existing_item():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            item_id = kwargs.get("item_id")
            item = ItemModel.find_by(id=item_id)
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
