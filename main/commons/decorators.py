from functools import wraps

# import jwt
from flask import request

# from main import app
from main.commons.exceptions import BadRequest, Unauthorized
from main.libs.utils import decode_jwt_token
from main.models.user import UserModel


def validate_input(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        pass


def jwt_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            raise Unauthorized()
        try:
            payload = decode_jwt_token(token)
            current_user = UserModel.find_by(id=payload["sub"])
        except Exception:
            raise BadRequest()
        return func(current_user, *args, **kwargs)

    return decorator


def check_is_owner(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        pass
