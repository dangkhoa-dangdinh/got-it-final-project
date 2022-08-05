from main import app
from main.commons.decorators import (
    check_existing_category,
    check_existing_item,
    check_owner,
    jwt_required,
    validate_input,
)
from main.commons.exceptions import ItemAlreadyExists, MissingAllFields
from main.models.item import ItemModel
from main.models.pagination import PaginationModel
from main.schemas.base import PaginationSchema
from main.schemas.item import ItemListSchema, ItemSchema, ItemUpdateSchema


@app.route("/categories/<int:category_id>/items", methods=["GET"])
@check_existing_category()
@validate_input(PaginationSchema)
def get_item_list(category_id, data, **__):
    page = data.get("page")
    per_page = data.get("per_page")
    pagination = ItemModel.paginate_items(page, per_page, category_id)
    items = pagination.items

    pagination_model = PaginationModel(
        pagination.page, pagination.per_page, pagination.total, items
    )
    response = ItemListSchema().dump(pagination_model)
    return response


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@jwt_required
@validate_input(ItemSchema)
@check_existing_category()
@check_owner
def post_item(category_id, data, **__):
    name = data.get("name")
    description = data.get("description")

    if ItemModel.find_by(name=name):
        raise ItemAlreadyExists()

    item = ItemModel(name=name, description=description, category_id=category_id)
    item.save_to_db()
    return {}


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
@check_existing_category()
@check_existing_item()
def get_item(item, **__):
    return ItemSchema().dump(item)


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required
@validate_input(ItemUpdateSchema)
@check_existing_category()
@check_existing_item()
@check_owner
def put_item(item, data, **__):

    if ItemModel.find_by(**data):
        raise ItemAlreadyExists()

    if data == {}:
        raise MissingAllFields()

    item.update_to_db(item.id, **data)

    return {}


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required
@check_existing_category()
@check_existing_item()
@check_owner
def delete_item(item, **__):
    item.delete_from_db()
    return {}
