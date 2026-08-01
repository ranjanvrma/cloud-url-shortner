import hashlib
import secrets
import string

from app.extensions import db
from app.models import URL

_ALPHABET = string.ascii_letters + string.digits
_MAX_ATTEMPTS = 10


def hash_url(original_url):
    return hashlib.sha256(original_url.encode("utf-8")).hexdigest()


def generate_short_code(length):
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def generate_unique_short_code(length):
    for _ in range(_MAX_ATTEMPTS):
        code = generate_short_code(length)
        exists = db.session.query(URL.id).filter_by(short_code=code).first()
        if exists is None:
            return code
    raise RuntimeError("Unable to generate a unique short code after multiple attempts")
