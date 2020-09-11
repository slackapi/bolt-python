import logging
import os
from logging import Logger
from typing import Optional, List, Dict, Callable

from slack_bolt.error import BoltError
from slack_bolt.oauth.callback_options import (
    FailureArgs,
    SuccessArgs,
    DefaultCallbackOptions,
    CallbackOptions,
)

from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.errors import SlackApiError
from slack_sdk.oauth import OAuthStateUtils
from slack_sdk.oauth.installation_store import Installation
from slack_sdk.oauth.installation_store.sqlite3 import SQLite3InstallationStore
from slack_sdk.oauth.state_store.sqlite3 import SQLite3OAuthStateStore
from slack_sdk.web import WebClient, SlackResponse

from slack_bolt.util.utils import create_web_client


class OAuthFlow:
    settings: OAuthSettings
    client_id: str
    redirect_uri: Optional[str]
    install_path: str
    redirect_uri_path: str

    success_handler: Callable[[SuccessArgs], BoltResponse]
    failure_handler: Callable[[FailureArgs], BoltResponse]

    @property
    def client(self) -> WebClient:
        if self._client is None:
            self._client = create_web_client()
        return self._client

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
        return self._logger

    def __init__(
        self,
        *,
        client: Optional[WebClient] = None,
        logger: Optional[Logger] = None,
        settings: OAuthSettings,
    ):
        self._client = client
        self._logger = logger
        self.settings = settings
        self.client_id = self.settings.client_id
        self.redirect_uri = self.settings.redirect_uri
        self.install_path = self.settings.install_path
        self.redirect_uri_path = self.settings.redirect_uri_path

        if settings.callback_options is None:
            settings.callback_options = DefaultCallbackOptions(
                logger=logger,
                state_utils=self.settings.state_utils,
                redirect_uri_page_renderer=self.settings.redirect_uri_page_renderer,
            )
        self.success_handler = settings.callback_options.success
        self.failure_handler = settings.callback_options.failure

    # -----------------------------
    # Factory Methods
    # -----------------------------

    @classmethod
    def sqlite3(
        cls,
        database: str,
        # OAuth flow parameters/credentials
        client_id: Optional[str] = None,  # required
        client_secret: Optional[str] = None,  # required
        scopes: Optional[List[str]] = None,
        user_scopes: Optional[List[str]] = None,
        redirect_uri: Optional[str] = None,
        # Handler configuration
        install_path: Optional[str] = None,
        redirect_uri_path: Optional[str] = None,
        callback_options: Optional[CallbackOptions] = None,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        authorization_url: Optional[str] = None,
        # Installation Management
        # state parameter related configurations
        state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
        client: Optional[WebClient] = None,
        logger: Optional[Logger] = None,
    ) -> "OAuthFlow":

        client_id = client_id or os.environ["SLACK_CLIENT_ID"]  # required
        client_secret = client_secret or os.environ["SLACK_CLIENT_SECRET"]  # required
        scopes = scopes or os.environ.get("SLACK_SCOPES", "").split(",")
        user_scopes = user_scopes or os.environ.get("SLACK_USER_SCOPES", "").split(",")
        redirect_uri = redirect_uri or os.environ.get("SLACK_REDIRECT_URI", None)
        return OAuthFlow(
            client=client or WebClient(),
            logger=logger,
            settings=OAuthSettings(
                # OAuth flow parameters/credentials
                client_id=client_id,
                client_secret=client_secret,
                scopes=scopes,
                user_scopes=user_scopes,
                redirect_uri=redirect_uri,
                # Handler configuration
                install_path=install_path,
                redirect_uri_path=redirect_uri_path,
                callback_options=callback_options,
                success_url=success_url,
                failure_url=failure_url,
                authorization_url=authorization_url,
                # Installation Management
                installation_store=SQLite3InstallationStore(
                    database=database, client_id=client_id, logger=logger,
                ),
                # state parameter related configurations
                state_store=SQLite3OAuthStateStore(
                    database=database,
                    expiration_seconds=state_expiration_seconds,
                    logger=logger,
                ),
                state_cookie_name=state_cookie_name,
                state_expiration_seconds=state_expiration_seconds,
            ),
        )

    # -----------------------------
    # Installation
    # -----------------------------

    def handle_installation(self, request: BoltRequest) -> BoltResponse:
        state = self.issue_new_state(request)
        return self.build_authorize_url_redirection(request, state)

    # ----------------------
    # Internal methods for Installation

    def issue_new_state(self, request: BoltRequest) -> str:
        return self.settings.state_store.issue()

    def build_authorize_url_redirection(
        self, request: BoltRequest, state: str
    ) -> BoltResponse:
        return BoltResponse(
            status=302,
            headers={
                "Location": [self.settings.authorize_url_generator.generate(state)],
                "Set-Cookie": [
                    self.settings.state_utils.build_set_cookie_for_new_state(state)
                ],
            },
        )

    # -----------------------------
    # Callback
    # -----------------------------

    def handle_callback(self, request: BoltRequest) -> BoltResponse:

        # failure due to end-user's cancellation or invalid redirection to slack.com
        error = request.query.get("error", [None])[0]
        if error is not None:
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason=error,
                    suggested_status_code=200,
                    settings=self.settings,
                )
            )

        # state parameter verification
        state = request.query.get("state", [None])[0]
        if not self.settings.state_utils.is_valid_browser(state, request.headers):
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason="invalid_browser",
                    suggested_status_code=400,
                    settings=self.settings,
                )
            )

        valid_state_consumed = self.settings.state_store.consume(state)
        if not valid_state_consumed:
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason="invalid_state",
                    suggested_status_code=401,
                    settings=self.settings,
                )
            )

        # run installation
        code = request.query.get("code", [None])[0]
        if code is None:
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason="missing_code",
                    suggested_status_code=401,
                    settings=self.settings,
                )
            )

        installation = self.run_installation(code)
        if installation is None:
            # failed to run installation with the code
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason="invalid_code",
                    suggested_status_code=401,
                    settings=self.settings,
                )
            )

        # persist the installation
        try:
            self.store_installation(request, installation)
        except BoltError as err:
            return self.failure_handler(
                FailureArgs(
                    request=request,
                    reason="storage_error",
                    error=err,
                    suggested_status_code=500,
                    settings=self.settings,
                )
            )

        # display a successful completion page to the end-user
        return self.success_handler(
            SuccessArgs(
                request=request, installation=installation, settings=self.settings,
            )
        )

    # ----------------------
    # Internal methods for Callback

    def run_installation(self, code: str) -> Optional[Installation]:
        try:
            oauth_response: SlackResponse = self.client.oauth_v2_access(
                code=code,
                client_id=self.settings.client_id,
                client_secret=self.settings.client_secret,
                redirect_uri=self.settings.redirect_uri,  # can be None
            )
            installed_enterprise: Dict[str, str] = oauth_response.get(
                "enterprise"
            ) or {}
            installed_team: Dict[str, str] = oauth_response.get("team") or {}
            installer: Dict[str, str] = oauth_response.get("authed_user") or {}
            incoming_webhook: Dict[str, str] = oauth_response.get(
                "incoming_webhook"
            ) or {}

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

    def store_installation(self, request: BoltRequest, installation: Installation):
        # may raise BoltError
        self.settings.installation_store.save(installation)
