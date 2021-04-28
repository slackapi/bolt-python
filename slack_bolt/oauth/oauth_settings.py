import logging
import os
from logging import Logger
from typing import Optional, Sequence, Union

from slack_sdk.oauth import (
    OAuthStateStore,
    InstallationStore,
    OAuthStateUtils,
    AuthorizeUrlGenerator,
    RedirectUriPageRenderer,
)
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.authorization.authorize import Authorize, InstallationStoreAuthorize
from slack_bolt.error import BoltError
from slack_bolt.oauth.internals import get_or_create_default_installation_store
from slack_bolt.oauth.callback_options import CallbackOptions


class OAuthSettings:
    # OAuth flow parameters/credentials
    client_id: str
    client_secret: str
    scopes: Optional[Sequence[str]]
    user_scopes: Optional[Sequence[str]]
    redirect_uri: Optional[str]
    # Handler configuration
    install_path: str
    install_page_rendering_enabled: bool
    redirect_uri_path: str
    callback_options: Optional[CallbackOptions] = None
    success_url: Optional[str]
    failure_url: Optional[str]
    authorization_url: str  # default: https://slack.com/oauth/v2/authorize
    # Installation Management
    installation_store: InstallationStore
    installation_store_bot_only: bool
    authorize: Authorize
    # state parameter related configurations
    state_store: OAuthStateStore
    state_cookie_name: str
    state_expiration_seconds: int
    # Customizable utilities
    state_utils: OAuthStateUtils
    authorize_url_generator: AuthorizeUrlGenerator
    redirect_uri_page_renderer: RedirectUriPageRenderer
    # Others
    logger: Logger

    def __init__(
        self,
        *,
        # OAuth flow parameters/credentials
        client_id: Optional[str] = None,  # required
        client_secret: Optional[str] = None,  # required
        scopes: Optional[Union[Sequence[str], str]] = None,
        user_scopes: Optional[Union[Sequence[str], str]] = None,
        redirect_uri: Optional[str] = None,
        # Handler configuration
        install_path: str = "/slack/install",
        install_page_rendering_enabled: bool = True,
        redirect_uri_path: str = "/slack/oauth_redirect",
        callback_options: Optional[CallbackOptions] = None,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        authorization_url: Optional[str] = None,
        # Installation Management
        installation_store: Optional[InstallationStore] = None,
        installation_store_bot_only: bool = False,
        # state parameter related configurations
        state_store: Optional[OAuthStateStore] = None,
        state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
        # Others
        logger: Logger = logging.getLogger(__name__),
    ):
        """The settings for Slack App installation (OAuth flow).

        Args:
            client_id: Check the value in Settings > Basic Information > App Credentials
            client_secret: Check the value in Settings > Basic Information > App Credentials
            scopes: Check the value in Settings > Manage Distribution
            user_scopes: Check the value in Settings > Manage Distribution
            redirect_uri: Check the value in Features > OAuth & Permissions > Redirect URLs
            install_path: The endpoint to start an OAuth flow (Default: `/slack/install`)
            install_page_rendering_enabled: Renders a web page for install_path access if True
            redirect_uri_path: The path of Redirect URL (Default: `/slack/oauth_redirect`)
            callback_options: Give success/failure functions f you want to customize callback functions.
            success_url: Set a complete URL if you want to redirect end-users when an installation completes.
            failure_url: Set a complete URL if you want to redirect end-users when an installation fails.
            authorization_url: Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`
            installation_store: Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)
            installation_store_bot_only: Use `InstallationStore#find_bot()` if True (Default: False)
            state_store: Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)
            state_cookie_name: The cookie name that is set for installers' browser. (Default: "slack-app-oauth-state")
            state_expiration_seconds: The seconds that the state value is alive (Default: 600 seconds)
            logger: The logger that will be used internally
        """
        client_id: Optional[str] = client_id or os.environ.get("SLACK_CLIENT_ID")
        client_secret: Optional[str] = client_secret or os.environ.get(
            "SLACK_CLIENT_SECRET"
        )
        if client_id is None or client_secret is None:
            raise BoltError("Both client_id and client_secret are required")
        self.client_id = client_id
        self.client_secret = client_secret

        self.scopes = scopes or os.environ.get("SLACK_SCOPES", "").split(",")
        if isinstance(self.scopes, str):
            self.scopes = self.scopes.split(",")
        self.user_scopes = user_scopes or os.environ.get("SLACK_USER_SCOPES", "").split(
            ","
        )
        if isinstance(self.user_scopes, str):
            self.user_scopes = self.user_scopes.split(",")
        self.redirect_uri = redirect_uri or os.environ.get("SLACK_REDIRECT_URI")
        # Handler configuration
        self.install_path = install_path or os.environ.get(
            "SLACK_INSTALL_PATH", "/slack/install"
        )
        self.install_page_rendering_enabled = install_page_rendering_enabled
        self.redirect_uri_path = redirect_uri_path or os.environ.get(
            "SLACK_REDIRECT_URI_PATH", "/slack/oauth_redirect"
        )
        self.callback_options = callback_options
        self.success_url = success_url
        self.failure_url = failure_url
        self.authorization_url = (
            authorization_url or "https://slack.com/oauth/v2/authorize"
        )
        # Installation Management
        self.installation_store = (
            installation_store or get_or_create_default_installation_store(client_id)
        )
        self.installation_store_bot_only = installation_store_bot_only
        self.authorize = InstallationStoreAuthorize(
            logger=logger,
            installation_store=self.installation_store,
            bot_only=self.installation_store_bot_only,
        )
        # state parameter related configurations
        self.state_store = state_store or FileOAuthStateStore(
            expiration_seconds=state_expiration_seconds,
            client_id=client_id,
        )
        self.state_cookie_name = state_cookie_name
        self.state_expiration_seconds = state_expiration_seconds

        self.state_utils = OAuthStateUtils(
            cookie_name=self.state_cookie_name,
            expiration_seconds=self.state_expiration_seconds,
        )
        self.authorize_url_generator = AuthorizeUrlGenerator(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scopes=self.scopes,
            user_scopes=self.user_scopes,
            authorization_url=self.authorization_url,
        )
        self.redirect_uri_page_renderer = RedirectUriPageRenderer(
            install_path=self.install_path,
            redirect_uri_path=self.redirect_uri_path,
            success_url=self.success_url,
            failure_url=self.failure_url,
        )
