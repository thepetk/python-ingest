import os

from datetime import timedelta
from dotenv import load_dotenv


class Config(object):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Flask app Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_CONNECTION_STRING = ['postgresql://', os.getenv('DB_USER'), ':', os.getenv('DB_KEY'), '@localhost/ingest_db']
    SQLALCHEMY_DATABASE_URI = ''.join(DB_CONNECTION_STRING)

    # Tests Configuration
    TESTS_URL = 'https://127.0.0.1:5000'

    # RabbitMQ Configuration
    RMQ_HOST = os.getenv('RMQ_HOST')
    RMQ_PORT = os.getenv('RMQ_PORT')
    RMQ_USERNAME = os.getenv('RMQ_USERNAME')
    RMQ_PASSWORD = os.getenv('RMQ_PASSWORD')
    RMQ_QUEUE = os.getenv('RMQ_QUEUE')
    RMQ_RETRY = os.getenv('RMQ_RETRY')

    # Host Configuration
    INGEST_HOST = os.getenv('INGEST_HOST')
    INGEST_PORT = os.getenv('INGEST_PORT')
    RECONNECT_TIMEOUT = os.getenv('RECONNECT_TIMEOUT')
