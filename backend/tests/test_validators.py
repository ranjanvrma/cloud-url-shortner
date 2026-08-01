import pytest

from app.utils.validators import URLValidationError, validate_url


def test_valid_http_url():
    assert validate_url("http://example.com") == "http://example.com"


def test_valid_https_url():
    assert validate_url("https://example.com/path?x=1") == "https://example.com/path?x=1"


def test_strips_whitespace():
    assert validate_url("  https://example.com  ") == "https://example.com"


@pytest.mark.parametrize(
    "bad_url",
    [
        "",
        None,
        "not-a-url",
        "ftp://example.com",
        "javascript:alert(1)",
        "http://",
        "x" * 3000,
    ],
)
def test_rejects_invalid_urls(bad_url):
    with pytest.raises(URLValidationError):
        validate_url(bad_url)
