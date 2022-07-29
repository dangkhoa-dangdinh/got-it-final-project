from flask import jsonify, request

from main import app

from ..models.user_model import UserModel


@app.route("/users/signup", methods=["POST"])
def sign_up_user():
    data = request.get_json()
    user = UserModel(**data)
    user.save_to_db()
    return jsonify(user.convert_to_dict()), 201


@app.route("/users/auth", methods=["POST"])
def authenticate_user():
    pass
