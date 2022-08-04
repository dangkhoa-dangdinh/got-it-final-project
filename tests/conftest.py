import json
import os
import sys
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from main import app as _app
from main import db
from tests.helper import setup_db

if os.getenv("ENVIRONMENT") != "test":
    print('Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = (
    (Path(__file__) / ".." / ".." / "migrations" / "alembic.ini").resolve().as_posix()
)


@pytest.fixture(scope="session", autouse=True)
def app():
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session", autouse=True)
def recreate_database(app):
    db.reflect()
    db.drop_all()
    _config = Config(ALEMBIC_CONFIG)
    upgrade(_config, "heads")

    db.create_all()
    setup_db()


@pytest.fixture(scope="function", autouse=True)
def session(monkeypatch):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def client(app, session):
    return app.test_client()


@pytest.fixture(scope="function")
def get_application_json_header():
    return [("Content-Type", "application/json;")]


@pytest.fixture(scope="function")
def successful_authenticate(client, get_application_json_header):
    log_in_data = {"email": "a@gmail.com", "password": "Abc123"}  # user_id: 1
    log_in_request = client.post(
        "/users/auth", data=json.dumps(log_in_data), headers=get_application_json_header
    )
    jwt_token = json.loads(log_in_request.data.decode())["access_token"]
    print(jwt_token)

    return jwt_token
