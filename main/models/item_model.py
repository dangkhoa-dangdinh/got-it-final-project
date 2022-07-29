from main import db


class ItemModel(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    time_updated = db.Column(db.DateTime, onupdate=db.func.now(), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("CategoryModel")

    def __init__(
        self, _id, name, description, category_id, user_id, time_created, time_updated
    ):
        self.id = _id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.user_id = user_id
        self.time_created = time_created
        self.time_updated = time_updated

    def save_to_db(self):
        db.session.save(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
