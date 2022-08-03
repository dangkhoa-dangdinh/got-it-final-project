from flask import request

from main import app
from main.commons.decorators import jwt_required
from main.commons.exceptions import BadRequest, Forbidden, InternalServerError, NotFound
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.base import PaginationSchema
from main.schemas.item import ItemSchema


@app.route("/categories/<int:category_id>/items", methods=["GET"])
def get_item_list(category_id):
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
        pagination = ItemModel.paginate_items(page, per_page, category_id)
        items = pagination.items
        if items:
            response = {"items": [ItemSchema().dump(item) for item in items]}
        else:
            response = {"items": []}
        response.update(PaginationSchema().dump(pagination))
        return response
    except ValueError:
        raise BadRequest()


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required
def post_item(user_id, category_id):
    # Validation
    post_data = ItemSchema().load(request.get_json())
    name = post_data["name"]
    if ItemModel.find_by(name=name):
        raise BadRequest(error_message="An item with the same name already exists")
    description = post_data["description"]

    # Check authorization
    current_category = CategoryModel.find_by(id=category_id)

    if current_category:
        if current_category.user_id != user_id:
            raise Forbidden()
        else:
            if name and description:
                new_item = ItemModel(
                    name=name, description=description, category_id=category_id
                )
                try:
                    new_item.save_to_db()
                    return {}, 201
                except Exception:
                    raise InternalServerError()
            else:
                raise BadRequest(error_message="Missing required fields")
    else:
        raise NotFound(error_message="Category not found")


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
def get_item(category_id, item_id):
    item = (
        ItemModel.find_by(category_id=category_id).filter_by(id=item_id).one_or_none()
    )
    if item:
        return ItemSchema().dump(item), 201
    raise NotFound()


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required
def put_item(user_id, category_id, item_id):
    post_data = ItemSchema().load(request.get_json())

    name = post_data.get("name")
    description = post_data.get("description")

    item = (
        ItemModel.find_by(category_id=category_id).filter_by(id=item_id).one_or_none()
    )

    if item:
        if item.category.user_id != user_id:
            raise Forbidden()
        else:
            if description:
                item.description = description
            elif name:
                item.name = name
            else:
                raise BadRequest(error_message="All fields are missing")
    else:
        item = ItemModel(name=name, description=description, category_id=category_id)
        item.save_to_db()
        return {}, 201


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required
def delete_item(user_id, category_id, item_id):
    item = (
        ItemModel.find_by(category_id=category_id).filter_by(id=item_id).one_or_none()
    )
    if item:
        if item.category.user_id == user_id:
            item.delete_from_db()
            return {}, 201
        else:
            raise Forbidden()
    else:
        raise NotFound()
