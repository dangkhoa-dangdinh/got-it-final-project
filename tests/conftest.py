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
def item_test_data():
    return {
        "category_id": 1,
        "item_id": 1,
        "post_data": {"name": "new_item", "description": "new_desc"},
    }


@pytest.fixture(scope="function")
def successful_authentication(client):
    log_in_data = {"email": "a@gmail.com", "password": "Abc123"}  # user_id: 1
    log_in_response = client.post("/users/auth", json=log_in_data)
    jwt_token = log_in_response.json
    return [("Authorization", f"Bearer {jwt_token['access_token']}")]
