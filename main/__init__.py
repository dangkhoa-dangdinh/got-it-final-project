from importlib import import_module

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .commons.error_handlers import register_error_handlers
from .config import config

app = Flask(__name__)
app.config.from_object(config)
app.config["SECRET_KEY"] = "key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


register_subpackages()
register_error_handlers(app)
