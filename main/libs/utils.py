from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import sha512
from os import urandom

import jwt


def generate_random_salt():
    return b64encode(urandom(64)).decode("utf-8")


def generate_hashed_password(password, salt):
    hashed_password = sha512(
        b"%b" % bytes(password + salt, "utf-8"),
    )
    return hashed_password.hexdigest()


def generate_jwt_token(user_id):
    from main import app

    payload = {
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "sub": user_id,
    }
    token = jwt.encode(
        payload=payload, key=app.config.get("JWT_SECRET_KEY"), algorithm="HS256"
    )
    return token


def decode_jwt_token(token):
    from main import app

    try:
        payload = jwt.decode(
            jwt=token,
            key=app.config.get("JWT_SECRET_KEY"),
            algorithms="HS256",
            options={"verify_signature": True, "verify_exp": True},
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return {"message": "Access Token Expired"}, 401
    except jwt.InvalidTokenError:
        return {"message": "Invalid token"}, 400
