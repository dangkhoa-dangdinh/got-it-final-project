from main import app
from main.commons.decorators import (
    check_existing_category,
    check_owner,
    jwt_required,
    validate_input,
)
from main.commons.exceptions import CategoryAlreadyExists
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.pagination import PaginationModel
from main.schemas.base import PaginationSchema
from main.schemas.category import CategoryListSchema, CategorySchema


@app.route("/categories", methods=["GET"])
@validate_input(PaginationSchema)
def get_category_list(data):
    page = data.get("page")
    per_page = data.get("per_page")
    pagination = CategoryModel.paginate_categories(page, per_page)
    items = pagination.items

    pagination_model = PaginationModel(
        pagination.page, pagination.per_page, pagination.total, items
    )
    response = CategoryListSchema().dump(pagination_model)
    return response


@app.route("/categories", methods=["POST"])
@jwt_required
@validate_input(CategorySchema)
def post_category(user_id, data):
    name = data.get("name")
    if CategoryModel.find_by(name=name):
        raise CategoryAlreadyExists()

    category = CategoryModel(name=name, user_id=user_id)
    category.save_to_db()
    return {}


@app.route("/categories/<int:category_id>", methods=["GET"])
@check_existing_category()
def get_category(category, **__):
    return CategorySchema().dump(category)


@app.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required
@check_existing_category()
@check_owner
def delete_category(category, category_id, **__):
    for item in ItemModel.find_by(category_id=category_id).all():
        item.delete_from_db()
    category.delete_from_db()
    return {}
