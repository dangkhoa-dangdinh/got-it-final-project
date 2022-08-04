import hmac

from main import db
from main.libs.utils import generate_hashed_password, generate_random_salt


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    def __init__(self, email, password):
        self.email = email
        self.salt = generate_random_salt()
        self.hashed_password = generate_hashed_password(password, self.salt)

    @classmethod
    def find_by(cls, **kwargs):
        if "email" in kwargs.keys():
            return cls.query.filter_by(email=kwargs["email"]).one_or_none()
        elif "id" in kwargs.keys():
            return cls.query.filter_by(id=kwargs["id"]).one_or_none()

    def validate_password(self, password):
        password_to_check = generate_hashed_password(password, self.salt)
        if hmac.compare_digest(password_to_check, self.hashed_password):
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
