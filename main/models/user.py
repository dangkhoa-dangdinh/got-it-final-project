# from datetime import datetime, timedelta

from main import db
from main.libs.utils import (  # generate_jwt_token,
    generate_hashed_password,
    generate_random_salt,
)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    time_updated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    def __init__(self, email, password):
        self.email = email
        self.salt = generate_random_salt()
        self.hashed_password = generate_hashed_password(password, self.salt)

    # Put Schema here
    def convert_to_dict(self):
        return {"email": self.email, "id": self.id}

    @classmethod
    def find_by(cls, **kwargs):
        if "email" in kwargs.keys():
            return cls.query.filter_by(email=kwargs["email"]).first()
        elif "id" in kwargs.keys():
            return cls.query.filter_by(id=kwargs["id"]).first()
        return None

    def validate_user(self, password):
        hashed_password = generate_hashed_password(password, self.salt)
        if hashed_password == self.hashed_password:
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
