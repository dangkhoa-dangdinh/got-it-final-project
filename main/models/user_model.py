from main import db

from ..libs import utils


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    time_updated = db.Column(db.DateTime, onupdate=db.func.now(), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.salt = utils.generate_random_salt()
        self.hashed_password = utils.generate_hashed_password(password, self.salt)
        self.time_created = self.time_updated = db.func.now()

    # Put Schema here
    def convert_to_dict(self):
        return {"email": self.email, "id": self.id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
