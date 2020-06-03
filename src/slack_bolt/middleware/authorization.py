from typing import Callable

from slack_bolt.auth.result import AuthorizationResult
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .middleware import Middleware
from ..logger import get_bolt_logger


class SingleTeamAuthorization(Middleware):
    def __init__(self, client: WebClient):
        self.client = client
        self.logger = get_bolt_logger(SingleTeamAuthorization)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if _is_url_verification(req) or _is_ssl_check(req):
            return next()
        try:
            auth_result = self.client.auth_test()
            if auth_result:
                req.context["authorization_result"] = AuthorizationResult(
                    enterprise_id=auth_result.get("enterprise_id", None),
                    team_id=auth_result.get("team_id", None),
                    user_id=auth_result.get("user_id", None),
                    bot_id=auth_result.get("bot_id", None),
                )
            return next()
        except SlackApiError as e:
            self.logger.error(f"Failed to authorize with the given token ({e})")
            return BoltResponse(status=401, body=":x: Please install this app into the workspace :bow:")

# TODO: implement this
class MultiTeamsAuthorization(Middleware):
    def __init__(self):
        self.logger = get_bolt_logger(MultiTeamsAuthorization)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        return next()


# ----------------------------

def _is_url_verification(req: BoltRequest) -> bool:
    return req \
           and req.payload \
           and req.payload.get("type", None) == "url_verification"


def _is_ssl_check(req: BoltRequest) -> bool:
    return req \
           and req.payload \
           and req.payload.get("type", None) == "ssl_check"
