import logging
import os
from logging.handlers import RotatingFileHandler


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


def setup_logging(app):

    log_file = os.path.join(
        LOG_DIR,
        "app.log"
    )

    app.logger.setLevel(
        logging.INFO
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    existing_handler = None

    for handler in app.logger.handlers:

        if isinstance(
            handler,
            RotatingFileHandler
        ):
            existing_handler = handler
            break

    if existing_handler is None:

        handler = RotatingFileHandler(
            log_file,
            maxBytes=2 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        handler.setFormatter(
            formatter
        )

        handler.setLevel(
            logging.INFO
        )

        app.logger.addHandler(
            handler
        )

    app.logger.info(
        "Application logging initialized."
    )
