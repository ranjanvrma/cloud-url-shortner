from urllib.parse import urlparse

_ALLOWED_SCHEMES = {"http", "https"}
_MAX_URL_LENGTH = 2048


class URLValidationError(ValueError):
    pass


def validate_url(raw_url):
    if not raw_url or not isinstance(raw_url, str):
        raise URLValidationError("URL is required")

    raw_url = raw_url.strip()

    if len(raw_url) == 0:
        raise URLValidationError("URL is required")

    if len(raw_url) > _MAX_URL_LENGTH:
        raise URLValidationError(f"URL must be at most {_MAX_URL_LENGTH} characters")

    parsed = urlparse(raw_url)

    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise URLValidationError("URL must start with http:// or https://")

    if not parsed.netloc:
        raise URLValidationError("URL must include a valid host")

    return raw_url
