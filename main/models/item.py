from main import db


class ItemModel(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("CategoryModel", back_populates="items")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def paginate_items(cls, page, per_page, category_id):
        return cls.find_by(category_id=category_id).paginate(
            page, per_page, max_per_page=20, error_out=True
        )

    @classmethod
    def find_by(cls, **kwargs):
        if "name" in kwargs:
            return cls.query.filter_by(name=kwargs["name"]).one_or_none()
        elif "id" in kwargs:
            return cls.query.filter_by(id=kwargs["id"]).one_or_none()
        elif "category_id" in kwargs:
            return cls.query.filter_by(category_id=kwargs["category_id"])

    def update_to_db(self, item_id, **kwargs):
        self.query.filter_by(id=item_id).update(dict(kwargs))
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
