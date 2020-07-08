import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(**kwargs):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    return app

app = create_app()
db = SQLAlchemy(app)

ingest_logger = logging.getLogger('ingest_logger')
app.logger.handlers.extend(ingest_logger.handlers)
logging.getLogger().setLevel(logging.INFO)

# From our point of view this is one of the simplest
# though productive init files.
from app.routes import routes
