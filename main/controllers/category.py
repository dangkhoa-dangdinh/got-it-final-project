from flask import request

from main import app
from main.commons.decorators import jwt_required
from main.libs.utils import decode_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel


@app.route("/categories", methods=["GET"])
def get_category_list():
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))

        categories = CategoryModel.query.paginate(
            page, per_page, error_out=True
        ).query.all()
        if categories:
            return {
                "categories": [category.json() for category in categories],
                "page": page,
                "per_page": per_page,
                "total_items": len(categories),
            }

    except ValueError:
        return {"message": "Bad Request"}, 400


# POST - STILL HAVE 401 UNCHECKED
@app.route("/categories", methods=["POST"])
@jwt_required
def post_category():
    request_body = request.get_json()
    name = request_body["name"]
    if CategoryModel.find_by_name(name):
        return {"message": f"A category with the name {name} already exists."}, 400
    user_id = decode_jwt_token(request.headers["Authorization"])["id"]
    new_category = CategoryModel(name=name, user_id=user_id)
    try:
        new_category.save_to_db()
    except Exception as e:
        return {"message": f"Unexpected error in inserting item {str(e)}"}, 500
    return {}, 201


@app.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    category = CategoryModel.find_by_id(category_id)
    if category:
        return category.json(), 201
    return {"message": "Category with id not found"}, 404


# DELETE - STILL HAVE 401 NOT CHECKED
@app.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required
def delete_category(category_id: int):
    category = CategoryModel.find_by_id(category_id)
    if category:
        user_id = decode_jwt_token(request.headers["Authorization"])["id"]
        if user_id == category.category_id:
            category.delete_from_db()
            for item in ItemModel.find_by_category_id(category_id).all():
                item.delete_from_db()
        else:
            return {"message": "Forbidden"}, 403
    else:
        return {"message": "Category with id not found"}, 404
    return {}, 201
