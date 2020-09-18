import os
from typing import List, Optional

from slack_sdk.oauth import (
    OAuthStateStore,
    InstallationStore,
    OAuthStateUtils,
    AuthorizeUrlGenerator,
    RedirectUriPageRenderer,
)
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.error import BoltError
from slack_bolt.oauth.callback_options import CallbackOptions


class OAuthSettings:
    # OAuth flow parameters/credentials
    client_id: str
    client_secret: str
    scopes: Optional[List[str]]
    user_scopes: Optional[List[str]]
    redirect_uri: Optional[str]
    # Handler configuration
    install_path: str
    redirect_uri_path: str
    callback_options: Optional[CallbackOptions] = None
    success_url: Optional[str]
    failure_url: Optional[str]
    authorization_url: str  # default: https://slack.com/oauth/v2/authorize
    # Installation Management
    installation_store: InstallationStore
    # state parameter related configurations
    state_store: OAuthStateStore
    state_cookie_name: str
    state_expiration_seconds: int
    # Customizable utilities
    state_utils: OAuthStateUtils
    authorize_url_generator: AuthorizeUrlGenerator
    redirect_uri_page_renderer: RedirectUriPageRenderer

    def __init__(
        self,
        *,
        # OAuth flow parameters/credentials
        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = None,
        user_scopes: Optional[List[str]] = None,
        redirect_uri: Optional[str] = None,
        # Handler configuration
        install_path: str = "/slack/install",
        redirect_uri_path: str = "/slack/oauth_redirect",
        callback_options: Optional[CallbackOptions] = None,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        authorization_url: Optional[str] = None,
        # Installation Management
        installation_store: Optional[InstallationStore] = None,
        # state parameter related configurations
        state_store: Optional[OAuthStateStore] = None,
        state_cookie_name: str = OAuthStateUtils.default_cookie_name,
        state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
    ):
        self.client_id = client_id or os.environ.get("SLACK_CLIENT_ID", None)
        self.client_secret = client_secret or os.environ.get(
            "SLACK_CLIENT_SECRET", None
        )
        if self.client_id is None or self.client_secret is None:
            raise BoltError("Both client_id and client_secret are required")

        self.scopes = scopes or os.environ.get("SLACK_SCOPES", "").split(",")
        self.user_scopes = user_scopes or os.environ.get("SLACK_USER_SCOPES", "").split(
            ","
        )
        self.redirect_uri = redirect_uri or os.environ.get("SLACK_REDIRECT_URI", None)
        # Handler configuration
        self.install_path = install_path or os.environ.get(
            "SLACK_INSTALL_PATH", "/slack/install"
        )
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
        self.installation_store = installation_store or FileInstallationStore(
            client_id=client_id
        )
        # state parameter related configurations
        self.state_store = state_store or FileOAuthStateStore(
            expiration_seconds=state_expiration_seconds, client_id=client_id,
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
