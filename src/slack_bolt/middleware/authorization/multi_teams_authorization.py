from typing import Callable, Optional

from slack import WebClient

from slack_bolt.auth.result import AuthorizationResult
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from slack_sdk.installation_store import InstallationStore, Bot
from . import Authorization
from ...logger import get_bolt_logger


class MultiTeamsAuthorization(Authorization):
    def __init__(self, installation_store: InstallationStore):
        self.installation_store = installation_store
        self.logger = get_bolt_logger(MultiTeamsAuthorization)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if self.is_no_auth_required(req):
            return next()
        try:
            bot: Optional[Bot] = self.installation_store.find_bot(
                enterprise_id=req.context.enterprise_id,
                team_id=req.context.team_id,
            )
            if bot is None:
                return self.build_error_response()

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
                req.context["client"] = WebClient(token=bot.bot_token)
                return next()
            else:
                self.logger.error("Somehow, the auth.test is unexpectedly None")
                return self.build_error_response()

        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return self.build_error_rfesponse()
