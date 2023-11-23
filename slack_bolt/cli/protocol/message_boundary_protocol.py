import logging
from .protocol import Protocol


class MessageBoundaryProtocol(Protocol):
    name: str = "message-boundaries"

    def __init__(self, boundary):
        self.boundary = boundary

    def debug(self, msg: str, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        logging.error(msg, *args, **kwargs)

    def respond(self, data: str):
        print(self.boundary + data + self.boundary)
