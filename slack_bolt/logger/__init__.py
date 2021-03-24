"""Bolt for Python relies on the standard `logging` module."""

import logging
from logging import Logger
from typing import Any


def get_bolt_logger(cls: Any) -> Logger:
    logger = logging.getLogger(f"slack_bolt.{cls.__name__}")
    logger.disabled = logging.root.disabled
    logger.level = logging.root.level
    return logger


def get_bolt_app_logger(app_name: str, cls: object = None) -> Logger:
    if cls and hasattr(cls, "__name__"):
        logger = logging.getLogger(f"{app_name}:{cls.__name__}")
        logger.disabled = logging.root.disabled
        logger.level = logging.root.level
        return logger
    else:
        logger = logging.getLogger(app_name)
        logger.disabled = logging.root.disabled
        logger.level = logging.root.level
        return logger
