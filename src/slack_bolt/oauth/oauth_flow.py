from logging import Logger
from typing import Optional, List, Dict

from slack_bolt.errors import BoltError
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.installation_store import InstallationStore, Installation
from slack_sdk.oauth_state_store import OAuthStateStore


class OAuthFlow:

    def __init__(
        self,
        *,
        client: WebClient,
        logger: Logger,

        installation_store: InstallationStore,
        oauth_state_store: OAuthStateStore,
        oauth_state_cookie_name: str = "slack-app-oauth-state",
        oauth_state_expiration_seconds: int = 60 * 10,  # 10 minutes

        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = None,
        user_scopes: Optional[List[str]] = None,
        redirect_uri: Optional[str] = None,

        install_path: str = "/slack/install",
        redirect_uri_path: str = "/slack/oauth_redirect",

        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
    ):
        self.client = client
        self.logger = logger

        self.installation_store = installation_store
        self.oauth_state_store = oauth_state_store
        self.oauth_state_cookie_name = oauth_state_cookie_name
        self.oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.user_scopes = user_scopes
        self.redirect_uri = redirect_uri

        self.install_path = install_path
        self.redirect_uri_path = redirect_uri_path
        self.success_url = success_url
        self.failure_url = failure_url

    # -----------------------------
    # Installation
    # -----------------------------

    def handle_installation(self, request: BoltRequest) -> BoltResponse:
        state = self.oauth_state_store.issue()
        url = self.generate_installation_url(state)
        # build Set-Cookie value
        cookie_name = self.oauth_state_cookie_name
        max_age = self.oauth_state_expiration_seconds
        set_cookie = f"{cookie_name}={state}; " \
                     "Secure; " \
                     "HttpOnly; " \
                     "Path=/; " \
                     f"Max-Age={max_age}"

        return BoltResponse(
            status=302,
            body="",
            headers={"Location": url, "Set-Cookie": set_cookie},
        )

    def generate_installation_url(self, state: str):
        scopes = ",".join(self.scopes) if self.scopes else ""
        user_scopes = ",".join(self.user_scopes) if self.user_scopes else ""
        url = "https://slack.com/oauth/v2/authorize?" \
              f"state={state}&" \
              f"client_id={self.client_id}&" \
              f"scope={scopes}&" \
              f"user_scope={user_scopes}"
        if self.redirect_uri is not None:
            url += f"&redirect_uri={self.redirect_uri}"
        return url

    # -----------------------------
    # Callback
    # -----------------------------

    def handle_callback(self, request: BoltRequest) -> BoltResponse:
        error = request.query.get("error", None)
        if error is not None:
            return self.handle_callback_failure(request, reason=error, status=200)

        state = request.query.get("state", None)
        if not self.is_valid_browser(state, request.headers):
            return self.handle_callback_failure(request, reason="invalid_browser", status=400)
        valid_state_consumed = self.oauth_state_store.consume(state)
        if not valid_state_consumed:
            return self.handle_callback_failure(request, reason="invalid_state", status=401)

        code = request.query.get("code", None)
        if code is None:
            return self.handle_callback_failure(request, reason="invalid_code", status=401)
        installation = self.complete_installation(code)
        if installation is None:
            return self.handle_callback_failure(request, reason="invalid_code", status=401)

        try:
            self.store_installation(request, installation)
        except BoltError as e:
            return self.handle_callback_failure(request, reason="storage_error", error=e)

        return self.handle_callback_success(request, installation)

    def handle_callback_success(
        self,
        request: BoltRequest,
        installation: Installation,
    ) -> BoltResponse:
        debug_message = f"Handling an OAuth callback success (request: {request.query})"
        self.logger.debug(debug_message)

        url = self.success_url
        if url is None:
            if installation.team_id is None:
                url = "slack://open"
            else:
                url = f"slack://app?team={installation.team_id}&id={installation.app_id}"
        html = self.render_callback_success_html(url)
        return BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html",
                "Content-Length": len(html),
                "Set-Cookie": self.header_value_for_cookie_deletion(),
            },
            body=html,
        )

    def handle_callback_failure(
        self,
        request: BoltRequest,
        reason: str,
        status: int = 500,
        error: Optional[Exception] = None) -> BoltResponse:
        debug_message = "Handling an OAuth callback failure " \
                        f"(reason: {reason}, error: {error}, request: {request.query})"
        self.logger.debug(debug_message)
        html = self.render_callback_failure_html(reason)
        return BoltResponse(
            status=status,
            headers={
                "Content-Type": "text/html",
                "Content-Length": len(html),
                "Set-Cookie": self.header_value_for_cookie_deletion(),
            },
            body=html,
        )

    def complete_installation(self, code: str) -> Optional[Installation]:
        try:
            oauth_response = self.client.oauth_v2_access(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,  # can be None
                code=code
            )
            installed_enterprise: dict = oauth_response.get("enterprise", {})
            installed_team: dict = oauth_response.get("team", {})
            installer: dict = oauth_response.get("authed_user", {})
            webhook: dict = oauth_response.get("incoming_webhook", {})

            bot_token: Optional[str] = oauth_response.get("access_token", None)
            # NOTE: oauth.v2.access doesn't include bot_id in response
            bot_id: Optional[str] = None
            if bot_token is not None:
                auth_test = self.client.auth_test(token=bot_token)
                bot_id = auth_test["bot_id"]

            return Installation(
                app_id=oauth_response.get("app_id", None),
                enterprise_id=installed_enterprise.get("id", None),
                team_id=installed_team.get("id", None),
                bot_token=bot_token,
                bot_id=bot_id,
                bot_user_id=oauth_response.get("bot_user_id", None),
                bot_scopes=oauth_response.get("scope", None),  # comma-separated string
                user_id=installer.get("id", None),
                user_token=installer.get("access_token", None),
                user_scopes=installer.get("scope", None),  # comma-separated string
                incoming_webhook_url=webhook.get("url", None),
                incoming_webhook_channel_id=webhook.get("channel_id", None),
                incoming_webhook_configuration_url=webhook.get("configuration_url", None),
            )

        except SlackApiError as e:
            message = f"Failed to fetch oauth.v2.access result with code: {code} - error: {e}"
            self.logger.warning(message)
            return None

    def store_installation(self, request: BoltRequest, installation: Installation):
        # may raise BoltError
        self.installation_store.save(installation)

    def is_valid_browser(self, state: Optional[str], request_headers: Dict[str, str]) -> bool:
        if state is None \
            or request_headers is None \
            or request_headers.get("cookie", None) is None:
            return False
        for cookie in request_headers["cookie"]:
            if cookie == f"{self.oauth_state_cookie_name}={state}":
                return True
        return False

    def header_value_for_cookie_deletion(self):
        return f"{self.oauth_state_cookie_name}=deleted; " \
               "Secure; " \
               "HttpOnly; " \
               "Path=/; " \
               "Expires=Thu, 01 Jan 1970 00:00:00 GMT"


    def render_callback_success_html(self, url: str) -> str:
        return f"""
<html>
<head>
<meta http-equiv="refresh" content="0; URL={url}">
<style>
body {{
  padding: 10px 15px;
  font-family: verdana;
  text-align: center;
}}
</style>
</head>
<body>
<h2>Thank you!</h2>
<p>Redirecting to the Slack App... click <a href="{url}">here</a></p>
</body>
</html>
"""

    def render_callback_failure_html(self, reason: str) -> str:
        return f"""
<html>
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
<h2>Oops, Something Went Wrong!</h2>
<p>Please try again from <a href="{self.install_path}">here</a> or contact the app owner (reason: {reason})</p>
</body>
</html>
"""
