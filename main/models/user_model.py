from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    hashed_password = db.Column(db.String(256))
    salt = db.Column(db.String(256))

    def __init__(self, email, hashed_password, salt):
        self.email = email
        self.hashed_password = hashed_password
        self.salt = salt
