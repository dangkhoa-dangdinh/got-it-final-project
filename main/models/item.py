from main import db

# from main.commons.decorators import jwt_required


class ItemModel(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    time_updated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("CategoryModel", back_populates="items")

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)

    def json(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def find_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
