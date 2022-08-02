from flask import request

from main import app
from main.commons.decorators import jwt_required

# from main.commons.exceptions import Forbidden
from main.libs.utils import decode_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel


@app.route("/categories/<int:category_id>/items", methods=["GET"])
def get_item_list(category_id):
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
        items = (
            ItemModel.find_by_category_id(category_id)
            .paginate(page, per_page, error_out=True)
            .query.all()
        )
        if items:
            return {
                "items": [item.json() for item in items],
                "page": page,
                "per_page": per_page,
                "total_items": len(items),
            }
        return {"Message": "Category Not Found"}, 404
    except ValueError:
        return {"message": "Bad Request"}, 400


# POST - 401 UNCHECKED
@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required
def post_item(category_id):
    request_body = request.get_json()
    name = request_body["name"]
    if ItemModel.find_by_name(name):
        return {"message": f"An item with the name {name} already exists."}, 400
    description = request_body["description"]
    user_id = decode_jwt_token(request.headers["Authorization"])["id"]
    current_category = CategoryModel.find_by_id(category_id)
    if current_category:
        if current_category.user_id != user_id:
            return {"message": "Forbidden"}, 403
        else:
            if name and description:
                new_item = ItemModel(
                    name=name, description=description, category_id=category_id
                )
                try:
                    new_item.save_to_db()
                except Exception as e:
                    return {
                        "message": f"Unexpected error in inserting item {str(e)}"
                    }, 500
                return {}, 201
            else:
                return {"message": "Missing required fields"}, 400
    else:
        return {"message": "category not found"}, 404


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
def get_item(category_id, item_id):
    item = (
        ItemModel.find_by_category_id(category_id).filter_by(id=item_id).one_or_none()
    )
    if item:
        return item.json(), 201
    return {"message": "not found"}, 404


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required
def put_item(category_id, item_id, **kwargs):
    request_data = request.get_json()
    name = request_data["name"]
    description = request_data["description"]
    user_id = decode_jwt_token(request.headers["Authorization"])["id"]
    item = (
        ItemModel.find_by_category_id(category_id).filter_by(id=item_id).one_or_none()
    )
    current_category = CategoryModel.find_by_id(category_id)
    if current_category.user_id != user_id:
        return {"message": "forbidden"}, 403
    else:
        if item is None:
            item = ItemModel(name=name, description=description)
        else:
            if description:
                item.description = description
            elif name:
                item.name = name
            else:
                return {"message": "All fields are missing"}, 400
        item.save_to_db()
        return {}, 201


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required
def delete_item(category_id, item_id):
    user_id = decode_jwt_token(request.headers["Authorization"])["id"]
    item = (
        ItemModel.find_by_category_id(category_id).filter_by(id=item_id).one_or_none()
    )
    if item:
        if item.category.user_id == user_id:
            item.delete_from_db()
            return {}, 201
        else:
            return {"message": "Forbidden"}, 403
    else:
        return {"message": "not found"}, 404
