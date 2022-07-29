from functools import wraps

import jwt
from flask import jsonify, request

from main import app

from ..models.user_model import UserModel


def jwt_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing!!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = UserModel.query.filter_by(id=data["id"]).first()
        except Exception:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        return func(current_user, *args, **kwargs)

    return decorator
