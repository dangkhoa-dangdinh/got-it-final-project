from main import app
from main.commons.decorators import validate_input
from main.commons.exceptions import EmailAlreadyExists, InvalidEmailOrPassword
from main.libs.utils import generate_jwt_token
from main.models.user import UserModel
from main.schemas.user import LoginUserSchema, RegisterUserSchema


@app.route("/users/signup", methods=["POST"])
@validate_input(RegisterUserSchema)
def sign_up_user(data):
    email = data.get("email")
    password = data.get("password")

    user = UserModel.find_by(email=email)
    if user:
        raise EmailAlreadyExists()

    user = UserModel(email, password)
    user.save_to_db()
    jwt_token = generate_jwt_token(user.id)
    return {"access_token": jwt_token}


@app.route("/users/auth", methods=["POST"])
@validate_input(LoginUserSchema)
def authenticate_user(data):
    email = data.get("email")
    password = data.get("password")

    user = UserModel.find_by(email=email)
    if user and user.validate_password(password):
        jwt_token = generate_jwt_token(user.id)
        return {"access_token": jwt_token}
    raise InvalidEmailOrPassword()
