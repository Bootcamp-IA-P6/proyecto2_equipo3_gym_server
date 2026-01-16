import logging
from logging.config import dictConfig


def setup_logger():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
    })


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
