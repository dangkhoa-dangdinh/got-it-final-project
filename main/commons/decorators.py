from functools import wraps

from flask import request
from marshmallow import ValidationError as MarshmallowValidationError

from main.commons.exceptions import (
    BadRequest,
    CategoryNotFound,
    ForbiddenNotOwner,
    ItemNotFound,
    LackingAccessToken,
    ValidationError,
)
from main.libs.utils import decode_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel


def jwt_required(func):
    @wraps(func)
    def decorator(**kwargs):
        try:
            token = request.headers["Authorization"].split()[1]
        except Exception:
            raise LackingAccessToken()
        user_id = decode_jwt_token(token)
        return func(user_id=user_id, **kwargs)

    return decorator


def validate_input(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            data = _get_request_data(schema)
            return func(data=data, **kwargs)

        return wrapper

    return decorator


def check_existing_category(func):
    @wraps(func)
    def wrapper(**kwargs):
        category = CategoryModel.query.filter_by(id=kwargs["category_id"]).one_or_none()
        if not category:
            raise CategoryNotFound()
        return func(category=category, **kwargs)

    return wrapper


def check_existing_item(func):
    @wraps(func)
    def wrapper(**kwargs):
        item = ItemModel.query.filter_by(id=kwargs["item_id"]).one_or_none()
        if not item or kwargs["category"].id != item.category_id:
            raise ItemNotFound()
        return func(item=item, **kwargs)

    return wrapper


def check_owner(func):
    @wraps(func)
    def wrapper(**kwargs):
        if kwargs["category"].user_id != kwargs["user_id"]:
            raise ForbiddenNotOwner()
        return func(**kwargs)

    return wrapper


def _get_request_data(schema):
    try:
        if request.method in ("POST", "PUT"):
            data = request.get_json()
        else:
            data = request.args
        data = schema().load(data)
    except MarshmallowValidationError as error:
        raise ValidationError(error_message=error.messages)
    except BadRequest as error:
        raise BadRequest(error_message=str(error))

    return data
