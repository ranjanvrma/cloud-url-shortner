import pytest

from app import create_app
from app.config import Config
from app.extensions import db


class RateLimitedConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    BASE_URL = "http://testserver"
    RATE_LIMIT_SHORTEN = "2 per minute"
    TESTING = True


@pytest.fixture
def limited_client():
    application = create_app(RateLimitedConfig)
    with application.app_context():
        db.create_all()
        yield application.test_client()
        db.session.remove()
        db.drop_all()


def test_shorten_endpoint_enforces_rate_limit(limited_client):
    for _ in range(2):
        resp = limited_client.post(
            "/api/shorten", json={"url": "https://example.com/rl"}
        )
        assert resp.status_code in (200, 201)

    blocked = limited_client.post(
        "/api/shorten", json={"url": "https://example.com/rl2"}
    )
    assert blocked.status_code == 429
