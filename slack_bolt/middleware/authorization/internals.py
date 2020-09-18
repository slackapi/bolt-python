from typing import Optional, Union

from slack_sdk.web import SlackResponse

from slack_bolt.auth import AuthorizationResult
from slack_bolt.request.request import BoltRequest
from slack_bolt.response import BoltResponse


def _is_url_verification(req: BoltRequest) -> bool:
    return (
        req is not None
        and req.body is not None
        and req.body.get("type", None) == "url_verification"
    )


def _is_ssl_check(req: BoltRequest) -> bool:
    return (
        req is not None
        and req.body is not None
        and req.body.get("type", None) == "ssl_check"
    )


def _is_no_auth_required(req: BoltRequest) -> bool:
    return _is_url_verification(req) or _is_ssl_check(req)


def _build_error_response() -> BoltResponse:
    # show an ephemeral message to the end-user
    return BoltResponse(
        status=200, body=":x: Please install this app into the workspace :bow:",
    )


def _to_authorization_result(  # type: ignore
    auth_test_result: Union[SlackResponse, "AsyncSlackResponse"],
    bot_token: str,
    request_user_id: Optional[str],
):
    return AuthorizationResult(
        enterprise_id=auth_test_result.get("enterprise_id", None),
        team_id=auth_test_result.get("team_id", None),
        bot_user_id=auth_test_result.get("user_id", None),
        bot_id=auth_test_result.get("bot_id", None),
        bot_token=bot_token,
        user_id=request_user_id,
    )
