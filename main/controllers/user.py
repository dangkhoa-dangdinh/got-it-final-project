from flask import request

from main import app
from main.commons.exceptions import BadRequest
from main.libs.utils import generate_jwt_token
from main.models.user import UserModel
from main.schemas.user import UserSchema


@app.route("/users/signup", methods=["POST"])
def sign_up_user():
    user_schema = UserSchema()
    post_data = user_schema.dumps(request.get_json())
    user = UserModel.find_by(email=post_data.get("email"))
    if user:
        raise BadRequest()
    user = UserModel(email=post_data.get("email"), password=post_data.get("password"))
    user.save_to_db()
    jwt_token = generate_jwt_token(user.id).get("sub")
    return {"access-token": jwt_token}, 201


@app.route("/users/auth", methods=["POST"])
def authenticate_user():
    post_data = request.get_json()
    user = UserModel.find_by(email=post_data.get("email"))
    if user and user.validate_user(post_data.get("password")):
        jwt_token = generate_jwt_token(user.id).get("sub")
        if jwt_token:
            return {"access-token": jwt_token}, 201
    raise BadRequest()
