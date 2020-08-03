from typing import Callable

from slack_bolt.auth import AuthorizationResult
from slack_bolt.logger import get_bolt_logger
from slack_bolt.middleware.authorization import Authorization
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from .internals import _build_error_response, _is_no_auth_required


class SingleTeamAuthorization(Authorization):
    def __init__(self):
        self.logger = get_bolt_logger(SingleTeamAuthorization)

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if _is_no_auth_required(req):
            return next()
        try:
            auth_result = req.context.client.auth_test()
            if auth_result:
                req.context["authorization_result"] = AuthorizationResult(
                    enterprise_id=auth_result.get("enterprise_id", None),
                    team_id=auth_result.get("team_id", None),
                    bot_user_id=auth_result.get("user_id", None),
                    bot_id=auth_result.get("bot_id", None),
                    bot_token=req.context.client.token,
                    user_id=req.context.user_id,
                )
                return next()
            else:
                # Just in case
                self.logger.error("auth.test API call result is unexpectedly None")
                return _build_error_response()
        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
