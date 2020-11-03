from logging import Logger
from typing import Optional, Union

from slack_sdk.oauth import OAuthStateUtils, RedirectUriPageRenderer
from slack_sdk.oauth.installation_store import Installation

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class CallbackResponseBuilder:
    def __init__(
        self,
        *,
        logger: Logger,
        state_utils: OAuthStateUtils,
        redirect_uri_page_renderer: RedirectUriPageRenderer,
    ):
        self._logger = logger
        self._state_utils = state_utils
        self._redirect_uri_page_renderer = redirect_uri_page_renderer

    def _build_callback_success_response(  # type: ignore
        self,
        request: Union[BoltRequest, "AsyncBoltRequest"],
        installation: Installation,
    ) -> BoltResponse:
        debug_message = f"Handling an OAuth callback success (request: {request.query})"
        self._logger.debug(debug_message)

        html = self._redirect_uri_page_renderer.render_success_page(
            app_id=installation.app_id, team_id=installation.team_id,
        )
        return BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(bytes(html, "utf-8")),
                "Set-Cookie": self._state_utils.build_set_cookie_for_deletion(),
            },
            body=html,
        )

    def _build_callback_failure_response(  # type: ignore
        self,
        request: Union[BoltRequest, "AsyncBoltRequest"],
        reason: str,
        status: int = 500,
        error: Optional[Exception] = None,
    ) -> BoltResponse:
        debug_message = (
            "Handling an OAuth callback failure "
            f"(reason: {reason}, error: {error}, request: {request.query})"
        )
        self._logger.debug(debug_message)

        html = self._redirect_uri_page_renderer.render_failure_page(reason)
        return BoltResponse(
            status=status,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(bytes(html, "utf-8")),
                "Set-Cookie": self._state_utils.build_set_cookie_for_deletion(),
            },
            body=html,
        )


def _build_default_install_page_html(url: str) -> str:
    return f"""<html>
<head>
<style>
body {{
  padding: 10px 15px;
  font-family: verdana;
  text-align: center;
}}
</style>
</head>
<body>
<h2>Slack App Installation</h2>
<p><a href="{url}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a></p>
</body>
</html>
"""
