import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_observability(app):
    """Configura los logs locales y el reporte de errores a Sentry."""
    log_directory = Path(app.root_path) / "logs"
    log_directory.mkdir(exist_ok=True)

    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_directory / "app.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)

    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(log_level)
    werkzeug_logger.addHandler(file_handler)

    sentry_dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("APP_ENV", "development")

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment,
            release=os.getenv("APP_VERSION"),
            send_default_pii=False,
            traces_sample_rate=0.0,
            integrations=[
                FlaskIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR,
                ),
            ],
        )

    app.logger.info(
        "observability_configured sentry_enabled=%s environment=%s",
        bool(sentry_dsn),
        environment,
    )
