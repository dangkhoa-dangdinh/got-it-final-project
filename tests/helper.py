from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def setup_db():
    setup_user()
    setup_category()
    setup_item()


def setup_user():
    users = [
        UserModel("a@gmail.com", "Abc123"),
        UserModel("b@gmail.com", "Def456"),
        UserModel("c@gmail.com", "Xyz789"),
    ]
    for user in users:
        user.save_to_db()


def setup_category():
    categories_1 = [CategoryModel(name=f"cate_1_{i}", user_id=1) for i in range(3)]
    categories_2 = [CategoryModel(name=f"cate_2_{i}", user_id=2) for i in range(3)]
    categories_3 = [CategoryModel(name=f"cate_3_{i}", user_id=3) for i in range(3)]
    for cate1, cate2, cate3 in zip(categories_1, categories_2, categories_3):
        cate1.save_to_db()
        cate2.save_to_db()
        cate3.save_to_db()


def setup_item():
    items_1 = [
        ItemModel(name=f"item_1_{i}", description=f"desc_1_{i}", category_id=1)
        for i in range(10)
    ]

    items_2 = [
        ItemModel(name=f"item_2_{i}", description=f"desc_2_{i}", category_id=2)
        for i in range(10)
    ]

    items_3 = [
        ItemModel(name=f"item_3_{i}", description=f"desc_3_{i}", category_id=3)
        for i in range(10)
    ]

    for item1, item2, item3 in zip(items_1, items_2, items_3):
        item1.save_to_db()
        item2.save_to_db()
        item3.save_to_db()
