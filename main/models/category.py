from main import db


class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    items = db.relationship("ItemModel", back_populates="category")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def paginate_categories(cls, page, per_page):
        return cls.query.paginate(page, per_page, max_per_page=20, error_out=True)

    @classmethod
    def find_by(cls, **kwargs):
        if "name" in kwargs:
            return cls.query.filter_by(name=kwargs["name"]).one_or_none()
        elif "id" in kwargs:
            return cls.query.filter_by(id=kwargs["id"]).one_or_none()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
