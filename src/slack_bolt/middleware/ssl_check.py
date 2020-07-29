from typing import Callable

from slack_bolt.logger import get_bolt_logger
from slack_bolt.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SslCheck(Middleware):
    def __init__(self, verification_token: str = None):
        self.verification_token = verification_token
        self.logger = get_bolt_logger(SslCheck)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if "ssl_check" in req.payload and req.payload["ssl_check"] == "1":
            if self.verification_token and \
                self.verification_token == req.payload["token"]:
                return BoltResponse(status=401, body={"error": "invalid verification token"})
            return BoltResponse(status=200, body="")
        else:
            return next()
