from typing import Callable, Dict, Any

from slack_sdk.signature import SignatureVerifier

from slack_bolt.logger import get_bolt_logger
from .middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class RequestVerification(Middleware):  # type: ignore
    def __init__(self, signing_secret: str):
        self.verifier = SignatureVerifier(signing_secret=signing_secret)
        self.logger = get_bolt_logger(RequestVerification)

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if self._can_skip(req.payload):
            return next()

        body = req.body
        timestamp = req.headers.get("x-slack-request-timestamp", ["0"])[0]
        signature = req.headers.get("x-slack-signature", [""])[0]
        if self.verifier.is_valid(body, timestamp, signature):
            return next()
        else:
            self._debug_log_error(signature, timestamp, body)
            return self._build_error_response()

    # -----------------------------------------

    @staticmethod
    def _can_skip(payload: Dict[str, Any]) -> bool:
        return payload is not None and payload.get("ssl_check", None) == "1"

    @staticmethod
    def _build_error_response() -> BoltResponse:
        return BoltResponse(status=401, body={"error": "invalid request"})

    def _debug_log_error(self, signature, timestamp, body) -> None:
        self.logger.info(
            "Invalid request signature detected "
            f"(signature: {signature}, timestamp: {timestamp}, body: {body})"
        )
