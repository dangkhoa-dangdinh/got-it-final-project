from base64 import b64encode
from hashlib import sha512
from os import urandom

import jwt

from main import app


def generate_random_salt():
    return b64encode(urandom(64)).decode("utf-8")


def generate_hashed_password(password: str, salt: str) -> str:

    hashed_password = sha512(
        b"%b" % bytes(password + salt, "utf-8"),
    )
    return hashed_password.hexdigest()


def generate_jwt_token(content):
    encoded_content = jwt.encode(
        content, app.config.get("SECRET_KEY"), algorithm="HS256"
    )
    token = str(encoded_content).split("'")
    return token
