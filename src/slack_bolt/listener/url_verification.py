from typing import Callable

from slack_bolt.listener import Listener
from slack_bolt.logger import get_bolt_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class UrlVerificationListener(Listener):
    def __init__(self):
        self.logger = get_bolt_logger(UrlVerificationListener)

    def __call__(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        done: Callable[[], None]) -> BoltResponse:

        if req.payload and req.payload.get("type", None) == "url_verification":
            done()
            return BoltResponse(status=200, body={"challenge": req.payload.get("challenge")})
        else:
            return resp
