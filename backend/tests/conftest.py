import pytest

from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    BASE_URL = "http://testserver"
    RATE_LIMIT_SHORTEN = "1000 per second"
    TESTING = True


@pytest.fixture
def app():
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
