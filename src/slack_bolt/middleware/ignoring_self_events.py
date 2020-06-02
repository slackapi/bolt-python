import logging
from typing import Callable

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .middleware import Middleware
from ..logger import get_bolt_logger


class IgnoringSelfEvents(Middleware):
    def __init__(self):
        self.logger = get_bolt_logger(IgnoringSelfEvents)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse]) -> BoltResponse:
        auth_result = req.context.authorization_result
        if auth_result is not None \
            and req.context.user_id == auth_result.user_id:
            if self.logger.level <= logging.DEBUG:
                event = req.payload["event"]
                self.logger.debug(f"Skipped self event: {event}")
            return req.context.ack()
        else:
            return next()
