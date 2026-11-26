from logging import Logger
from typing import Callable, Dict, Optional
from urllib.parse import parse_qsl

from slack_bolt.logger import get_bolt_logger
from slack_bolt.middleware.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SslCheck(Middleware):
    verification_token: Optional[str]
    logger: Logger

    def __init__(
        self,
        verification_token: Optional[str] = None,
        base_logger: Optional[Logger] = None,
    ):
        """Handles `ssl_check` requests.

        Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details.

        Args:
            verification_token: The verification token to check
                (optional as it's already deprecated - https://docs.slack.dev/authentication/verifying-requests-from-slack/#deprecation)
            base_logger: The base logger
        """  # noqa: E501
        self.verification_token = verification_token
        self.logger = get_bolt_logger(SslCheck, base_logger=base_logger)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        # As this method is not supposed to be invoked by bolt-python users,
        # the naming conflict with the built-in one affects
        # only the internals of this method
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        form_params = self._parse_form_params(req.raw_body)
        if self._is_ssl_check_request(form_params):
            if self._verify_token_if_needed(form_params):
                return self._build_error_response()
            return self._build_success_response()
        else:
            return next()

    # -----------------------------------------

    @staticmethod
    def _parse_form_params(raw_body: str) -> Dict[str, str]:
        return dict(parse_qsl(raw_body, keep_blank_values=True))

    @staticmethod
    def _is_ssl_check_request(body: dict):
        return "ssl_check" in body and body["ssl_check"] == "1"

    def _verify_token_if_needed(self, body: dict):
        return self.verification_token and self.verification_token == body["token"]

    @staticmethod
    def _build_success_response() -> BoltResponse:
        return BoltResponse(status=200, body="")

    @staticmethod
    def _build_error_response() -> BoltResponse:
        return BoltResponse(status=401, body={"error": "invalid verification token"})
