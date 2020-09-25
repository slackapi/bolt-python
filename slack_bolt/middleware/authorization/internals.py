from typing import Optional, Union

from slack_sdk.web import SlackResponse

from slack_bolt.authorization import AuthorizeResult
from slack_bolt.request.request import BoltRequest
from slack_bolt.response import BoltResponse


def _is_url_verification(req: BoltRequest) -> bool:
    return (
        req is not None
        and req.body is not None
        and req.body.get("type") == "url_verification"
    )


def _is_ssl_check(req: BoltRequest) -> bool:
    return (
        req is not None and req.body is not None and req.body.get("type") == "ssl_check"
    )


def _is_no_auth_required(req: BoltRequest) -> bool:
    return _is_url_verification(req) or _is_ssl_check(req)


def _build_error_response() -> BoltResponse:
    # show an ephemeral message to the end-user
    return BoltResponse(
        status=200, body=":x: Please install this app into the workspace :bow:",
    )


def _is_bot_token(token: Optional[str]) -> bool:
    return token is not None and token.startswith("xoxb-")


def _to_authorize_result(  # type: ignore
    auth_test_result: Union[SlackResponse, "AsyncSlackResponse"],
    token: Optional[str],
    request_user_id: Optional[str],
) -> AuthorizeResult:
    user_id = auth_test_result.get("user_id")
    return AuthorizeResult(
        enterprise_id=auth_test_result.get("enterprise_id"),
        team_id=auth_test_result.get("team_id"),
        bot_id=auth_test_result.get("bot_id"),
        bot_user_id=user_id if _is_bot_token(token) else None,
        bot_token=token if _is_bot_token(token) else None,
        user_id=request_user_id or (user_id if not _is_bot_token(token) else None),
        user_token=token if not _is_bot_token(token) else None,
    )
