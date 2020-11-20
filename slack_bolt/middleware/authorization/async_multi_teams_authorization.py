from typing import Callable, Optional, Awaitable

from slack_sdk.errors import SlackApiError
from slack_bolt.logger import get_bolt_logger
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .async_authorization import AsyncAuthorization
from .async_internals import _build_error_response, _is_no_auth_required
from .internals import _is_no_auth_test_call_required
from ...authorization import AuthorizeResult
from ...authorization.async_authorize import AsyncAuthorize


class AsyncMultiTeamsAuthorization(AsyncAuthorization):
    authorize: AsyncAuthorize

    def __init__(self, authorize: AsyncAuthorize):
        """Multi-workspace authorization.

        :param authorize: The function to authorize incoming requests from Slack.
        """
        self.authorize = authorize
        self.logger = get_bolt_logger(AsyncMultiTeamsAuthorization)

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if _is_no_auth_required(req):
            return await next()

        if _is_no_auth_test_call_required(req):
            req.context.set_authorize_result(
                AuthorizeResult(
                    enterprise_id=req.context.enterprise_id,
                    team_id=req.context.team_id,
                    user_id=req.context.user_id,
                )
            )
            return await next()

        try:
            auth_result: Optional[AuthorizeResult] = await self.authorize(
                context=req.context,
                enterprise_id=req.context.enterprise_id,
                team_id=req.context.team_id,
                user_id=req.context.user_id,
            )
            if auth_result:
                req.context.set_authorize_result(auth_result)
                token = auth_result.bot_token or auth_result.user_token
                req.context["token"] = token
                # As AsyncApp#_init_context() generates a new AsyncWebClient for this request,
                # it's safe to modify this instance.
                req.context.client.token = token
                return await next()
            else:
                # Just in case
                self.logger.error("auth.test API call result is unexpectedly None")
                return _build_error_response()

        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
