from typing import Callable

from slack_bolt.logger import get_bolt_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .middleware import Middleware


class UrlVerification(Middleware):
    def __init__(self):
        self.logger = get_bolt_logger(UrlVerification)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if req.payload and req.payload.get("type", None) == "url_verification":
            return BoltResponse(status=200, body={"challenge": req.payload.get("challenge")})
        else:
            return next()
        if self.can_skip(req.payload):
            return next()
