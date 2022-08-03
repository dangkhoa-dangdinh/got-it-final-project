import json

import pytest


class TestUser:
    accept_json = [("Content-Type", "application/json;")]

    def test_successful_sign_up(self, client):
        payload = dict(email="d@gmail.com", password="Abc123")
        request_body = client.post(
            "/users/signup", data=json.dumps(payload), headers=TestUser.accept_json
        )
        assert request_body.status_code == 201

    def test_successful_auth(self, client):
        payload = dict(email="a@gmail.com", password="Abc123")
        request_body = client.post(
            "/users/auth", data=json.dumps(payload), headers=TestUser.accept_json
        )
        assert request_body.status_code == 201

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
        payload = dict(email=email, password=password)
        sign_up_request_body = client.post(
            "/users/signup", data=json.dumps(payload), headers=TestUser.accept_json
        )
        assert sign_up_request_body.status_code == 400

    @pytest.mark.parametrize(
        "email, password",
        [
            ("a@gmail.com", "wrong_password"),  # Wrong password
            ("a@gmail.com", ""),  # Missing password
            ("agmail.com", "some_password"),  # Invalid email format
            ("a@gmailcom", "some_password"),  # Invalid email format
            ("d@gmail.com", "some_password"),  # Unregistered user
            ("", ""),  # Missing email & password
        ],
    )
    def test_invalid_auth(self, client, email, password):
        payload = dict(email=email, password=password)
        auth_request_body = client.post(
            "/users/auth", data=json.dumps(payload), headers=TestUser.accept_json
        )
        assert auth_request_body.status_code == 400
