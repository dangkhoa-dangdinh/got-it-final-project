from main import app


@app.route("/categories/<int:category_id>/items", methods=["GET"])
def get_item_list(category_id):
    pass


@app.route("/categories/<int:category_id>/items", methods=["POST"])
def post_item(category_id):
    pass


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
def get_item(category_id, item_id):
    pass


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
def put_item(category_id, item_id):
    pass


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item(category_id, item_id):
    pass
