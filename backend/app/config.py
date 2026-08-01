import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    _explicit_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if _explicit_uri:
        SQLALCHEMY_DATABASE_URI = _explicit_uri
    else:
        DB_USER = os.environ.get("DB_USER", "url_shortener_app")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
        DB_HOST = os.environ.get("DB_HOST", "localhost")
        DB_PORT = os.environ.get("DB_PORT", "3306")
        DB_NAME = os.environ.get("DB_NAME", "url_shortener")
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000").rstrip("/")
    SHORT_CODE_LENGTH = int(os.environ.get("SHORT_CODE_LENGTH", "7"))
    RATE_LIMIT_SHORTEN = os.environ.get("RATE_LIMIT_SHORTEN", "20 per minute")

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "logs/app.log")
