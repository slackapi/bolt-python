from typing import Callable, Optional

from slack_bolt.logger import get_bolt_logger
from .authorization import Authorization
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse
from .internals import (
    _build_error_response,
    _is_no_auth_required,
    _to_authorization_result,
)


class SingleTeamAuthorization(Authorization):
    def __init__(
        self,
        *,
        auth_test_result: Optional[SlackResponse] = None,
        verification_enabled: bool = True,
    ):
        self.auth_test_result = auth_test_result
        self.verification_enabled = verification_enabled
        self.logger = get_bolt_logger(SingleTeamAuthorization)

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if _is_no_auth_required(req):
            return next()

        if not self.verification_enabled:
            # Skip calling auth.test every time the app receives requests
            req.context["authorization_result"] = _to_authorization_result(
                auth_test_result=self.auth_test_result,
                bot_token=req.context.client.token,
                request_user_id=req.context.user_id,
            )
            return next()

        try:
            auth_result = req.context.client.auth_test()
            if auth_result:
                req.context["authorization_result"] = _to_authorization_result(
                    auth_test_result=auth_result,
                    bot_token=req.context.client.token,
                    request_user_id=req.context.user_id,
                )
                return next()
            else:
                # Just in case
                self.logger.error("auth.test API call result is unexpectedly None")
                return _build_error_response()
        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
