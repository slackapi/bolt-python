from typing import Callable

from slack_bolt.logger import get_bolt_logger
from .middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SslCheck(Middleware):  # type: ignore
    def __init__(self, verification_token: str = None):
        self.verification_token = verification_token
        self.logger = get_bolt_logger(SslCheck)

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if self._is_ssl_check_request(req.payload):
            if self._verify_token_if_needed(req.payload):
                return self._build_error_response()
            return self._build_success_response()
        else:
            return next()

    # -----------------------------------------

    @staticmethod
    def _is_ssl_check_request(payload: dict):
        return "ssl_check" in payload and payload["ssl_check"] == "1"

    def _verify_token_if_needed(self, payload: dict):
        return self.verification_token and self.verification_token == payload["token"]

    @staticmethod
    def _build_success_response() -> BoltResponse:
        return BoltResponse(status=200, body="")

    @staticmethod
    def _build_error_response() -> BoltResponse:
        return BoltResponse(status=401, body={"error": "invalid verification token"})
