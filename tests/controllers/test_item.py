import json

import pytest

category_id = 1
item_id = 1
post_data = {"name": "new_item", "description": "new_desc"}


class TestGetItem:
    # In catalog_test, item table have 90 items, 30 items belong to category_id 1,
    # 30 -> category_id 2, 30 -> category_id 3, max items per page should be 20,
    # so number of items of category_id 1 on page 1 should be 20, page 2 should be 10

    @pytest.mark.parametrize("page, per_page", [(1, 20), (2, 20)])
    def test_successful_pagination_get_item_lists(self, client, page, per_page):
        data = {
            "page": page,
            "per_page": per_page,
        }

        response = client.get(f"/categories/{category_id}/items", query_string=data)
        assert response.status_code == 200

        response_data = json.loads(response.data.decode())
        page = response_data["page"]
        numbers_of_categories_displayed = len(response_data["items"])
        if page == 1:
            assert numbers_of_categories_displayed == 20
        elif page == 2:
            assert numbers_of_categories_displayed == 10

    # Item with item_id 1 belongs to category_id 1
    def test_successful_get_one_item(self, client):
        response = client.get(f"/categories/{category_id}/items/{item_id}")
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
    def test_invalid_query_type_get_item_lists(self, client, page, per_page):
        data = {
            "page": page,
            "per_page": per_page,
        }
        response = client.get(f"/categories/{category_id}/items", query_string=data)
        assert response.status_code == 400

    # In catalog_test, item table have 90, max items per page should be 20,
    # so the number of items (of category_id 1) on page 1 should be 20,
    # page 2 should be 10, and page 3 should have no category,
    # thus lead to error not found (404)
    def test_invalid_query_page_number_item_lists(self, client):
        data = {"page": 3, "per_page": 20}
        response = client.get(f"/categories/{category_id}/items", query_string=data)
        assert response.status_code == 404

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

    # successful_authenticate -> jwt_token of user_id 1
    # successful when create item in category_id 1 (belongs to user_id 1)
    def test_successful_post_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.post(
            f"/categories/{category_id}/items",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "item_1_1", "description": "desc1"},  # Item name already exists
            {
                "name": "",
                "description": "sample_desc",
            },  # Missing required field (item name and description)
            {},
        ],
    )
    def test_invalid_post_item(
        self, client, successful_authenticate, get_application_json_header, data
    ):
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.post(
            f"/categories/{category_id}/items",
            data=json.dumps(data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_post_item(self, client, get_application_json_header):
        post_accept_json = get_application_json_header + [("Authorization", "")]
        post_response = client.post(
            f"/categories/{category_id}/items",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 401

    # successful_authenticate -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_post_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        forbidden_category_id = 2
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.post(
            f"/categories/{forbidden_category_id}/items",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 403

    def test_not_found_post_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        not_found_category_id = 31
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.post(
            f"/categories/{not_found_category_id}/items",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 404


class TestPutItem:
    def test_successful_put_item(
        self, client, get_application_json_header, successful_authenticate
    ):
        data = {"name": "updated__item", "description": "updated_description"}

        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.put(
            f"/categories/{category_id}/items/{item_id}",
            data=json.dumps(data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [{"name": "item_1_2", "description": "desc1"}, {}],  # Item name already exists
    )
    def test_invalid_put_item(
        self, client, successful_authenticate, get_application_json_header, data
    ):
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.put(
            f"/categories/{category_id}/items/{item_id}",
            data=json.dumps(data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 400

    # Lacking access_token
    def test_unauthorized_put_item(self, client, get_application_json_header):
        post_accept_json = get_application_json_header + [("Authorization", "")]
        post_response = client.put(
            f"/categories/{category_id}/items/{item_id}",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 401

    # successful_authenticate -> user_id 1
    # forbidden_category_id -> category_id 2 belongs to user_id 2
    def test_forbidden_put_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        forbidden_category_id = 2
        forbidden_item_id = 2
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.put(
            f"/categories/{forbidden_category_id}/items/{forbidden_item_id}",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 403

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(31, 1), (1, 2), (1, 91)]
    )
    def test_not_found_put_item(
        self,
        client,
        successful_authenticate,
        get_application_json_header,
        not_found_item_id,
        not_found_category_id,
    ):
        post_accept_json = get_application_json_header + [
            ("Authorization", successful_authenticate)
        ]
        post_response = client.put(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            data=json.dumps(post_data),
            headers=post_accept_json,
        )
        assert post_response.status_code == 404


class TestDeleteItem:
    def test_successful_delete_item(self, client, successful_authenticate):
        delete_accept_json = [("Authorization", successful_authenticate)]
        delete_response = client.delete(
            f"/categories/{category_id}/items/{item_id}", headers=delete_accept_json
        )
        assert delete_response.status_code == 200

    def test_unauthorized_delete_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        delete_accept_json = [("Authorization", "")]
        delete_response = client.delete(
            f"/categories/{category_id}/items/{item_id}", headers=delete_accept_json
        )
        assert delete_response.status_code == 401

    @pytest.mark.parametrize(
        "not_found_category_id, not_found_item_id", [(31, 1), (1, 2), (1, 91)]
    )
    def test_not_found_delete_item(
        self,
        client,
        successful_authenticate,
        get_application_json_header,
        not_found_item_id,
        not_found_category_id,
    ):
        delete_accept_json = [("Authorization", successful_authenticate)]
        delete_response = client.delete(
            f"/categories/{not_found_category_id}/items/{not_found_item_id}",
            headers=delete_accept_json,
        )
        assert delete_response.status_code == 404

    # In database, category_id 2 belongs to user_id 2
    # While successful_authenticate returns JWT token of user_id 1
    # So a Forbidden (403) error should be raised
    def test_not_owner_delete_item(
        self, client, successful_authenticate, get_application_json_header
    ):
        delete_category_id = 2
        delete_item_id = 2
        delete_accept_json = [("Authorization", successful_authenticate)]
        delete_response = client.delete(
            f"/categories/{delete_category_id}/items/{delete_item_id}",
            headers=delete_accept_json,
        )
        assert delete_response.status_code == 403
