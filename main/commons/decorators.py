from functools import wraps

from flask import request

from main.commons.exceptions import BadRequest, Unauthorized
from main.libs.utils import decode_jwt_token
from main.models.user import UserModel


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
            current_user_id = UserModel.find_by(id=payload).id
        except Exception:
            raise BadRequest()
        return func(current_user_id, *args, **kwargs)

    return decorator
