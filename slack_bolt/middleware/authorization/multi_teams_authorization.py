from typing import Callable, Optional

from slack_bolt.auth.result import AuthorizationResult
from slack_bolt.logger import get_bolt_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from slack_sdk.oauth.installation_store import InstallationStore, Bot
from .authorization import Authorization
from .internals import _build_error_response, _is_no_auth_required
from ...util.utils import create_web_client


class MultiTeamsAuthorization(Authorization):
    installation_store: InstallationStore
    verification_enabled: bool

    def __init__(
        self, installation_store: InstallationStore, verification_enabled: bool = True,
    ):
        self.installation_store = installation_store
        self.verification_enabled = verification_enabled
        self.logger = get_bolt_logger(MultiTeamsAuthorization)

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if _is_no_auth_required(req):
            return next()
        try:
            bot: Optional[Bot] = self.installation_store.find_bot(
                enterprise_id=req.context.enterprise_id, team_id=req.context.team_id,
            )
            if bot is None:
                return _build_error_response()

            if self.verification_enabled:
                auth_result = req.context.client.auth_test(token=bot.bot_token)
                if auth_result:
                    req.context["authorization_result"] = AuthorizationResult(
                        enterprise_id=auth_result.get("enterprise_id", None),
                        team_id=auth_result.get("team_id", None),
                        bot_user_id=auth_result.get("user_id", None),
                        bot_id=auth_result.get("bot_id", None),
                        bot_token=bot.bot_token,
                    )
                    # TODO: bot -> user token
                    req.context["token"] = bot.bot_token
                    req.context["client"] = create_web_client(bot.bot_token)
                    return next()
                else:
                    # Just in case
                    self.logger.error("auth.test API call result is unexpectedly None")
                    return _build_error_response()
            else:
                req.context["authorization_result"] = AuthorizationResult(
                    enterprise_id=bot.enterprise_id,
                    team_id=bot.team_id,
                    bot_user_id=bot.bot_user_id,
                    bot_id=bot.bot_id,
                    bot_token=bot.bot_token,
                )
                # TODO: bot -> user token
                req.context["token"] = bot.bot_token
                req.context["client"] = create_web_client(bot.bot_token)
                return next()

        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return _build_error_response()
