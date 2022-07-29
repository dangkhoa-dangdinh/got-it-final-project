from main import app

from ..models.category_model import CategoryModel


@app.route("/categories", methods=["GET"])
def get_category_list():
    pass


@app.route("/categories", methods=["POST"])
def post_category():
    pass


@app.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int) -> "CategoryModel":
    pass


@app.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int, access_token: str):
    pass
