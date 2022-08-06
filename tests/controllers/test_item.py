import pytest


class TestGetItem:
    # In catalog_test, item table have 90 items, 30 items belong to category_id 1,
    # 30 -> category_id 2, 30 -> category_id 3, max items per page should be 20,
    # so number of items of category_id 1 on page 1 should be 20, page 2 should be 10

    @pytest.mark.parametrize("page, per_page", [(1, 20), (2, 20)])
    def test_successful_pagination_get_item_lists(
        self, client, page, per_page, item_test_data
    ):
        data = {
            "page": page,
            "per_page": per_page,
        }

        response = client.get(
            f"/categories/{item_test_data['category_id']}/items", query_string=data
        )
        assert response.status_code == 200

        response_data = response.json
        page = response_data["page"]
        numbers_of_categories_displayed = len(response_data["items"])
        if page == 1:
            assert numbers_of_categories_displayed == 20
        elif page == 2:
            assert numbers_of_categories_displayed == 10

    # Item with item_id 1 belongs to category_id 1
    def test_successful_get_one_item(self, client, item_test_data):
        response = client.get(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}"
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "page, per_page",
        [
            (
                "a",
                "b",
            ),
            # Invalid type for query params (which should be integer)
            # =>  validation error (400)
            ("", ""),
            ("a", 2),
        ],
    )
    def test_invalid_query_type_get_item_lists(
        self, client, page, per_page, item_test_data
    ):
        data = {
            "page": page,
            "per_page": per_page,
        }
        response = client.get(
            f"/categories/{item_test_data['category_id']}/items", query_string=data
        )
        assert response.status_code == 400

    # In catalog_test, item table have 90, max items per page should be 20,
    # so the number of items (of category_id 1) on page 1 should be 20,
    # page 2 should be 10, and page 3 should have no category,
    # thus lead to empty items
    def test_invalid_query_page_number_item_lists(self, client, item_test_data):
        data = {"page": 3, "per_page": 20}
        response = client.get(
            f"/categories/{item_test_data['category_id']}/items", query_string=data
        )
        assert response.status_code == 200
        assert response.json["items"] == []

    def test_query_page_over_20_item_lists(self, client, item_test_data):
        data = {"page": 1, "per_page": 100}
        response = client.get(
            f"/categories/{item_test_data['category_id']}/items", query_string=data
        )
        assert response.status_code == 400

    # There are only 90 categories whose ids labeled from 1->90,
    # so no category with id 91 or "a" -> 404
    @pytest.mark.parametrize(
        "invalid_category_id, invalid_item_id", [(91, ""), ("a", 1), ("", "")]
    )
    def test_invalid_get_item(self, client, invalid_category_id, invalid_item_id):
        response = client.get(
            f"/categories/{invalid_category_id}/items/{invalid_item_id}"
        )
        assert response.status_code == 404


class TestPostItem:

    # successful_authentication -> jwt_token of user_id 1
    # successful when create item in category_id 1 (belongs to user_id 1)
    def test_successful_post_item(
        self, client, successful_authentication, item_test_data
    ):
        post_response = client.post(
            f"/categories/{item_test_data['category_id']}/items",
            json=item_test_data["post_data"],
            headers=successful_authentication,
        )
        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "item_1_1", "description": "desc1"},  # Item name already exists
            {
                "name": "",
                "description": "sample_desc",
            },
            {},  # Missing required field (item name and description)
        ],
    )
    def test_invalid_post_item(
        self, client, successful_authentication, data, item_test_data
    ):
        post_response = client.post(
            f"/categories/{item_test_data['category_id']}/items",
            json=data,
            headers=successful_authentication,
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_post_item(self, client, item_test_data):
        post_response = client.post(
            f"/categories/{item_test_data['category_id']}/items",
            json=item_test_data["post_data"],
            headers=[("Authorization", "Bearer ")],
        )
        assert post_response.status_code == 401

    # successful_authentication -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_post_item(
        self, client, successful_authentication, item_test_data
    ):
        forbidden_category_id = 2
        post_response = client.post(
            f"/categories/{forbidden_category_id}/items",
            json=item_test_data["post_data"],
            headers=successful_authentication,
        )
        assert post_response.status_code == 403

    def test_not_found_post_item(
        self, client, successful_authentication, item_test_data
    ):
        not_found_category_id = 31
        post_response = client.post(
            f"/categories/{not_found_category_id}/items",
            json=item_test_data["post_data"],
            headers=successful_authentication,
        )
        assert post_response.status_code == 404


class TestPutItem:
    def test_successful_put_item(
        self, client, successful_authentication, item_test_data
    ):
        data = {"name": "updated__item", "description": "updated_description"}

        post_response = client.put(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}",
            json=data,
            headers=successful_authentication,
        )
        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [{"name": "item_1_2", "description": "desc1"}, {}, {"random": "random"}],
    )
    def test_invalid_put_item(
        self, client, successful_authentication, data, item_test_data
    ):
        post_response = client.put(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}",
            json=data,
            headers=successful_authentication,
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_put_item(self, client, item_test_data):
        post_response = client.put(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}",
            json=item_test_data["post_data"],
            headers=[("Authorization", "Bearer ")],
        )
        assert post_response.status_code == 401

    # successful_authentication -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_put_item(
        self, client, successful_authentication, item_test_data
    ):
        forbidden_category_id = 2
        forbidden_item_id = 2
        post_response = client.put(
            f"/categories/{forbidden_category_id}/items/{forbidden_item_id}",
            json=item_test_data["post_data"],
            headers=successful_authentication,
        )
        assert post_response.status_code == 403

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(31, 1), (1, 2), (1, 91)]
    )
    def test_not_found_put_item(
        self,
        client,
        successful_authentication,
        not_found_item_id,
        not_found_category_id,
        item_test_data,
    ):
        post_response = client.put(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            json=item_test_data["post_data"],
            headers=successful_authentication,
        )
        assert post_response.status_code == 404


class TestDeleteItem:
    def test_successful_delete_item(
        self, client, successful_authentication, item_test_data
    ):
        delete_response = client.delete(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}",
            headers=successful_authentication,
        )

        assert delete_response.status_code == 200

    def test_unauthorized_delete_item(self, client, item_test_data):
        delete_response = client.delete(
            f"/categories/{item_test_data['category_id']}"
            f"/items/{item_test_data['item_id']}",
            headers="",
        )
        assert delete_response.status_code == 401

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(31, 1), (1, 91)]
    )
    def test_not_found_delete_item(
        self,
        client,
        successful_authentication,
        not_found_item_id,
        not_found_category_id,
    ):
        delete_response = client.delete(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            headers=successful_authentication,
        )
        assert delete_response.status_code == 404

    # In database, category_id 2 belongs to user_id 2
    # While successful_authentication returns JWT token of user_id 1
    # So a Forbidden (403) error should be raised
    def test_not_owner_delete_item(self, client, successful_authentication):
        delete_category_id = 2
        delete_item_id = 2
        delete_response = client.delete(
            f"/categories/{delete_category_id}/items/{delete_item_id}",
            headers=successful_authentication,
        )
        assert delete_response.status_code == 403

    def test_invalid_access_token(self, client, item_test_data):
        invalid_access_token = [("Authorization", "Bearer abc")]
        response = client.post(
            f"/categories/{item_test_data['category_id']}/items",
            json=item_test_data["post_data"],
            headers=invalid_access_token,
        )
        assert response.status_code == 400
