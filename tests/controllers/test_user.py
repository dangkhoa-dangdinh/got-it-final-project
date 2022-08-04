import json

import pytest


class TestUser:
    accept_json = [("Content-Type", "application/json;")]

    def test_successful_sign_up(self, client):
        data = {"email": "d@gmail.com", "password": "Abc123"}
        response = client.post(
            "/users/signup", data=json.dumps(data), headers=TestUser.accept_json
        )
        assert response.status_code == 200

    def test_successful_auth(self, client):
        data = {"email": "a@gmail.com", "password": "Abc123"}
        response = client.post(
            "/users/auth", data=json.dumps(data), headers=TestUser.accept_json
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "email, password",
        [
            ("a@gmail.com", "Abc123"),  # Email already exists
            ("agmail.com", "some_password"),  # Invalid email format
            ("a@gmailcom", "Abc123"),  # Invalid email format
            ("d@gmail.com", "abc123"),  # Password does not meet requirements
            ("d@gmail.com", "Abcdef"),  # Password does not meet requirements
            ("d@gmail.com", "123456"),  # Password does not meet requirements
            ("d@gmail.com", "ABC123"),  # Password does not meet requirements
            ("d@gmail.com", "Ab123"),  # Password does not meet requirements
            ("", ""),  # Invalid email, password
        ],
    )
    def test_invalid_sign_up(self, client, email, password):
        data = {"email": email, "password": password}
        response = client.post(
            "/users/signup", data=json.dumps(data), headers=TestUser.accept_json
        )
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "email, password",
        [
            ("a@gmail.com", "wrong_password"),  # Wrong password
            ("a@gmail.com", ""),  # Missing password
            ("agmail.com", "some_password"),  # Invalid email format
            ("a@gmailcom", "some_password"),  # Invalid email format
            ("d@gmail.com", "some_password"),  # Unregistered user
            ("", ""),  # Invalid email & password
        ],
    )
    def test_invalid_auth(self, client, email, password):
        data = {"email": email, "password": password}
        response = client.post(
            "/users/auth", data=json.dumps(data), headers=TestUser.accept_json
        )
        assert response.status_code == 400
