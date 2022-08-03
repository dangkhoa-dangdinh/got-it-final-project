from flask import request

from main import app
from main.commons.decorators import jwt_required
from main.commons.exceptions import BadRequest, Forbidden, InternalServerError, NotFound
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema


@app.route("/categories", methods=["GET"])
def get_category_list():
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
        pagination = CategoryModel.paginate_categories(page, per_page)
        categories = pagination.items
        if categories:
            response = {
                "categories": [
                    CategorySchema().dump(category) for category in categories
                ]
            }
            response.update(PaginationSchema().dump(pagination))
            return response
        else:
            return {}
    except ValueError:
        raise BadRequest()


@app.route("/categories", methods=["POST"])
@jwt_required
def post_category(user_id):
    post_data = CategorySchema().load(request.get_json())
    name = post_data.get("name")

    if CategoryModel.find_by(name=name):
        raise BadRequest(error_message="Category name already exists!")

    jwt_token = request.headers["Authorization"]

    if jwt_token:
        new_category = CategoryModel(name=name, user_id=user_id)
        try:
            new_category.save_to_db()
        except Exception:
            raise InternalServerError()
        return {}, 201
    else:
        raise BadRequest(error_message="Lacking access token")


@app.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    category = CategoryModel.find_by(id=category_id)
    if category:
        return CategorySchema().dump(category), 201
    raise NotFound(error_message="Category ID Not Found")


@app.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required
def delete_category(user_id, category_id):
    category = CategoryModel.find_by(id=category_id)
    if category:
        if user_id == category.user_id:
            category.delete_from_db()
            for item in ItemModel.find_by(category_id=category_id).all():
                item.delete_from_db()
        else:
            raise Forbidden(error_message="Only the owner of a category can delete it")
    else:
        raise NotFound(error_message="Category ID Not Found")
    return {}, 201
