import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    log_level = getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO)
    log_file = app.config["LOG_FILE"]

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
