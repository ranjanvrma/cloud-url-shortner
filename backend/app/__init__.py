from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, limiter, migrate
from app.logging_config import configure_logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
    app,
    resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}
)

    configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    from app.routes.api import api_bp
    from app.routes.redirect import redirect_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(redirect_bp)

    register_error_handlers(app)
    register_security_headers(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(err):
        return jsonify(error="Bad request"), 400

    @app.errorhandler(404)
    def not_found(err):
        return jsonify(error="Not found"), 404

    @app.errorhandler(429)
    def rate_limited(err):
        return jsonify(error="Rate limit exceeded, please try again later"), 429

    @app.errorhandler(500)
    def internal_error(err):
        app.logger.exception("Unhandled server error")
        return jsonify(error="Internal server error"), 500


def register_security_headers(app):
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
