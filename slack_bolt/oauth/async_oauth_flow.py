import logging
import os
from logging import Logger
from typing import Optional, List, Dict

from slack_bolt.error import BoltError
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from slack_sdk.oauth import (
    AuthorizeUrlGenerator,
    OAuthStateUtils,
    RedirectUriPageRenderer,
)
from slack_sdk.oauth.installation_store import Installation
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.oauth.installation_store.sqlite3 import SQLite3InstallationStore
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.oauth.state_store.sqlite3 import SQLite3OAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse

from slack_bolt.util.async_utils import create_async_web_client


class AsyncOAuthFlow:
    installation_store: AsyncInstallationStore
    oauth_state_store: AsyncOAuthStateStore
    oauth_state_cookie_name: str
    oauth_state_expiration_seconds: int

    client_id: str
    client_secret: str
    redirect_uri: Optional[str]
    scopes: Optional[List[str]]
    user_scopes: Optional[List[str]]

    install_path: str
    redirect_uri_path: str
    success_url: Optional[str]
    failure_url: Optional[str]
    oauth_state_utils: OAuthStateUtils
    authorize_url_generator: AuthorizeUrlGenerator
    redirect_uri_page_renderer: RedirectUriPageRenderer

    @property
    def client(self) -> AsyncWebClient:
        if self._async_client is None:
            self._async_client = create_async_web_client()
        return self._async_client

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
        return self._logger

    def __init__(
        self,
        *,
        client: Optional[AsyncWebClient] = None,
        logger: Optional[Logger] = None,
        installation_store: AsyncInstallationStore,
        oauth_state_store: AsyncOAuthStateStore,
        oauth_state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        oauth_state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
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
        self._async_client = client
        self._logger = logger

        self.installation_store = installation_store
        self.oauth_state_store = oauth_state_store
        self.oauth_state_cookie_name = oauth_state_cookie_name
        self.oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.user_scopes = user_scopes

        self.install_path = install_path
        self.redirect_uri_path = redirect_uri_path
        self.success_url = success_url
        self.failure_url = failure_url

        self._init_internal_utils()

    def _init_internal_utils(self):
        self.oauth_state_utils = OAuthStateUtils(
            cookie_name=self.oauth_state_cookie_name,
            expiration_seconds=self.oauth_state_expiration_seconds,
        )
        self.authorize_url_generator = AuthorizeUrlGenerator(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scopes=self.scopes,
            user_scopes=self.user_scopes,
        )
        self.redirect_uri_page_renderer = RedirectUriPageRenderer(
            install_path=self.install_path,
            redirect_uri_path=self.redirect_uri_path,
            success_url=self.success_url,
            failure_url=self.failure_url,
        )

    # -----------------------------
    # Factory Methods
    # -----------------------------

    @classmethod
    def sqlite3(
        cls,
        database: str,
        client_id: Optional[str] = os.environ.get("SLACK_CLIENT_ID", None),
        client_secret: Optional[str] = os.environ.get("SLACK_CLIENT_SECRET", None),
        scopes: List[str] = os.environ.get("SLACK_SCOPES", "").split(","),
        user_scopes: List[str] = os.environ.get("SLACK_USER_SCOPES", "").split(","),
        redirect_uri: Optional[str] = os.environ.get("SLACK_REDIRECT_URI", None),
        oauth_state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        oauth_state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
        logger: Optional[Logger] = None,
    ) -> "AsyncOAuthFlow":

        return AsyncOAuthFlow(
            client=create_async_web_client(),
            logger=logger,
            installation_store=SQLite3InstallationStore(
                database=database, client_id=client_id, logger=logger,
            ),
            oauth_state_store=SQLite3OAuthStateStore(
                database=database,
                expiration_seconds=oauth_state_expiration_seconds,
                logger=logger,
            ),
            oauth_state_cookie_name=oauth_state_cookie_name,
            oauth_state_expiration_seconds=oauth_state_expiration_seconds,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            user_scopes=user_scopes,
            redirect_uri=redirect_uri,
        )

    # -----------------------------
    # Installation
    # -----------------------------

    async def handle_installation(self, request: BoltRequest) -> BoltResponse:
        state = await self.issue_new_state(request)
        return await self.build_authorize_url_redirection(request, state)

    # ----------------------
    # Internal methods for Installation

    async def issue_new_state(self, request: BoltRequest) -> str:
        return await self.oauth_state_store.async_issue()

    async def build_authorize_url_redirection(
        self, request: BoltRequest, state: str
    ) -> BoltResponse:
        return BoltResponse(
            status=302,
            headers={
                "Location": [self.authorize_url_generator.generate(state)],
                "Set-Cookie": [
                    self.oauth_state_utils.build_set_cookie_for_new_state(state)
                ],
            },
        )

    # -----------------------------
    # Callback
    # -----------------------------

    async def handle_callback(self, request: BoltRequest) -> BoltResponse:

        # failure due to end-user's cancellation or invalid redirection to slack.com
        error = request.query.get("error", [None])[0]
        if error is not None:
            return await self.build_callback_failure_response(
                request, reason=error, status=200
            )

        # state parameter verification
        state = request.query.get("state", [None])[0]
        if not self.oauth_state_utils.is_valid_browser(state, request.headers):
            return await self.build_callback_failure_response(
                request, reason="invalid_browser", status=400
            )

        valid_state_consumed = await self.oauth_state_store.async_consume(state)
        if not valid_state_consumed:
            return await self.build_callback_failure_response(
                request, reason="invalid_state", status=401
            )

        # run installation
        code = request.query.get("code", [None])[0]
        if code is None:
            return await self.build_callback_failure_response(
                request, reason="missing_code", status=401
            )
        installation = await self.run_installation(code)
        if installation is None:
            # failed to run installation with the code
            return await self.build_callback_failure_response(
                request, reason="invalid_code", status=401
            )

        # persist the installation
        try:
            await self.store_installation(request, installation)
        except BoltError as e:
            return await self.build_callback_failure_response(
                request, reason="storage_error", error=e
            )

        # display a successful completion page to the end-user
        return await self.build_callback_success_response(request, installation)

    # ----------------------
    # Internal methods for Callback

    async def run_installation(self, code: str) -> Optional[Installation]:
        try:
            oauth_response: AsyncSlackResponse = await self.client.oauth_v2_access(
                code=code,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,  # can be None
            )
            installed_enterprise: Dict[str, str] = oauth_response.get("enterprise", {})
            installed_team: Dict[str, str] = oauth_response.get("team", {})
            installer: Dict[str, str] = oauth_response.get("authed_user", {})
            incoming_webhook: Dict[str, str] = oauth_response.get(
                "incoming_webhook", {}
            )

            bot_token: Optional[str] = oauth_response.get("access_token", None)
            # NOTE: oauth.v2.access doesn't include bot_id in response
            bot_id: Optional[str] = None
            if bot_token is not None:
                auth_test = await self.client.auth_test(token=bot_token)
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
                incoming_webhook_url=incoming_webhook.get("url", None),
                incoming_webhook_channel_id=incoming_webhook.get("channel_id", None),
                incoming_webhook_configuration_url=incoming_webhook.get(
                    "configuration_url", None
                ),
            )

        except SlackApiError as e:
            message = (
                f"Failed to fetch oauth.v2.access result with code: {code} - error: {e}"
            )
            self.logger.warning(message)
            return None

    async def store_installation(
        self, request: BoltRequest, installation: Installation
    ):
        # may raise BoltError
        await self.installation_store.async_save(installation)

    async def build_callback_failure_response(
        self,
        request: BoltRequest,
        reason: str,
        status: int = 500,
        error: Optional[Exception] = None,
    ) -> BoltResponse:
        debug_message = (
            "Handling an OAuth callback failure "
            f"(reason: {reason}, error: {error}, request: {request.query})"
        )
        self.logger.debug(debug_message)

        html = self.redirect_uri_page_renderer.render_failure_page(reason)
        return BoltResponse(
            status=status,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(html),
                "Set-Cookie": self.oauth_state_utils.build_set_cookie_for_deletion(),
            },
            body=html,
        )

    async def build_callback_success_response(
        self, request: BoltRequest, installation: Installation,
    ) -> BoltResponse:
        debug_message = f"Handling an OAuth callback success (request: {request.query})"
        self.logger.debug(debug_message)

        html = self.redirect_uri_page_renderer.render_success_page(
            app_id=installation.app_id, team_id=installation.team_id,
        )
        return BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(html),
                "Set-Cookie": self.oauth_state_utils.build_set_cookie_for_deletion(),
            },
            body=html,
        )
