from typing import Callable, Optional

from slack_sdk.errors import SlackApiError

from slack_bolt.logger import get_bolt_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .authorization import Authorization
from .internals import (
    _build_error_response,
    _is_no_auth_required,
    _is_no_auth_test_call_required,
)
from ...authorization import AuthorizeResult
from ...authorization.authorize import Authorize


class MultiTeamsAuthorization(Authorization):
    authorize: Authorize

    def __init__(
        self,
        *,
        authorize: Authorize,
    ):
        """Multi-workspace authorization.

        :param authorize: The function to authorize incoming requests from Slack.
        """
        self.authorize = authorize
        self.logger = get_bolt_logger(MultiTeamsAuthorization)

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
            auth_result: Optional[AuthorizeResult] = self.authorize(
                context=req.context,
                enterprise_id=req.context.enterprise_id,
                team_id=req.context.team_id,
                user_id=req.context.user_id,
            )
            if auth_result is not None:
                req.context.set_authorize_result(auth_result)
                token = auth_result.bot_token or auth_result.user_token
                req.context["token"] = token
                # As App#_init_context() generates a new WebClient for this request,
                # it's safe to modify this instance.
                req.context.client.token = token
                return next()
            else:
                # Just in case
                self.logger.error("auth.test API call result is unexpectedly None")
                return _build_error_response()

        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
