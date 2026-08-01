from flask import Blueprint, current_app, jsonify, request

from app.extensions import db, limiter
from app.models import URL
from app.utils.shortcode import generate_unique_short_code, hash_url
from app.utils.validators import URLValidationError, validate_url

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.post("/shorten")
@limiter.limit(lambda: current_app.config["RATE_LIMIT_SHORTEN"])
def shorten_url():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(error="Request body must be valid JSON"), 400

    try:
        original_url = validate_url(payload.get("url"))
    except URLValidationError as exc:
        return jsonify(error=str(exc)), 400

    url_hash = hash_url(original_url)

    existing = URL.query.filter_by(original_url_hash=url_hash).first()
    if existing is not None:
        return jsonify(existing.to_dict(current_app.config["BASE_URL"])), 200

    short_code = generate_unique_short_code(current_app.config["SHORT_CODE_LENGTH"])
    entry = URL(
        short_code=short_code,
        original_url=original_url,
        original_url_hash=url_hash,
    )
    db.session.add(entry)
    db.session.commit()

    current_app.logger.info("Created short code %s for %s", short_code, original_url)
    return jsonify(entry.to_dict(current_app.config["BASE_URL"])), 201


@api_bp.get("/stats/<string:short_code>")
def get_stats(short_code):
    entry = URL.query.filter_by(short_code=short_code).first()
    if entry is None:
        return jsonify(error="Short code not found"), 404

    return jsonify(entry.to_dict(current_app.config["BASE_URL"])), 200
