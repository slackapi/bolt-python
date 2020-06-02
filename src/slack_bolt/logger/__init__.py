import logging
from logging import Logger
from typing import Optional


def get_bolt_logger(cls: any) -> Logger:
    return logging.getLogger(f"slack_bolt.{cls.__name__}")


def get_bolt_app_logger(app_name: str, cls: Optional[any] = None) -> Logger:
    if cls and hasattr(cls, "__name__"):
        return logging.getLogger(f"{app_name}:{cls.__name__}")
    else:
        return logging.getLogger(app_name)
