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
    _to_authorize_result,
    _is_no_auth_test_call_required,
)
from ...authorization import AuthorizeResult


class SingleTeamAuthorization(Authorization):
    def __init__(self, *, auth_test_result: Optional[SlackResponse] = None):
        """Single-workspace authorization.

        Args:
            auth_test_result: The initial `auth.test` API call result.
        """
        self.auth_test_result = auth_test_result
        self.logger = get_bolt_logger(SingleTeamAuthorization)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if _is_no_auth_required(req):
            return next()

        if _is_no_auth_test_call_required(req):
            req.context.set_authorize_result(
                AuthorizeResult(
                    enterprise_id=req.context.enterprise_id,
                    team_id=req.context.team_id,
                    user_id=req.context.user_id,
                )
            )
            return next()

        try:
            if not self.auth_test_result:
                self.auth_test_result = req.context.client.auth_test()

            if self.auth_test_result:
                req.context.set_authorize_result(
                    _to_authorize_result(
                        auth_test_result=self.auth_test_result,
                        token=req.context.client.token,
                        request_user_id=req.context.user_id,
                    )
                )
                return next()
            else:
                # Just in case
                self.logger.error("auth.test API call result is unexpectedly None")
                return _build_error_response()
        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
