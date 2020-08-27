import logging
import os
from logging import Logger
from typing import Optional

import boto3

from slack_bolt.oauth import OAuthFlow
from slack_sdk import WebClient
from slack_sdk.oauth.installation_store.amazon_s3 import AmazonS3InstallationStore
from slack_sdk.oauth.state_store.amazon_s3 import AmazonS3OAuthStateStore

from slack_bolt.util.utils import create_web_client


class LambdaS3OAuthFlow(OAuthFlow):
    def __init__(
        self,
        *,
        client: Optional[WebClient] = None,
        logger: Optional[Logger] = None,
        oauth_state_bucket_name: Optional[str] = None,  # required
        installation_bucket_name: Optional[str] = None,  # required
        oauth_state_cookie_name: str = "slack-app-oauth-state",
        oauth_state_expiration_seconds: int = 60 * 10,  # 10 minutes
        client_id: Optional[str] = None,  # required
        client_secret: Optional[str] = None,  # required
        scopes: Optional[str] = None,  # required
        user_scopes: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        install_path: Optional[str] = None,  # required
        redirect_uri_path: Optional[str] = None,  # required
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
    ):
        self._client = client
        self._logger = logger

        self.s3_client = boto3.client("s3")

        oauth_state_bucket_name = (
            oauth_state_bucket_name
            or os.environ["SLACK_STATE_S3_BUCKET_NAME"]  # required
        )
        installation_bucket_name = (
            installation_bucket_name
            or os.environ["SLACK_INSTALLATION_S3_BUCKET_NAME"]  # required
        )

        client_id = client_id or os.environ["SLACK_CLIENT_ID"]  # required
        client_secret = client_secret or os.environ["SLACK_CLIENT_SECRET"]  # required
        scopes = scopes or os.environ.get("SLACK_SCOPES", None)
        user_scopes = user_scopes or os.environ.get("SLACK_USER_SCOPES", None)
        redirect_uri = redirect_uri or os.environ.get("SLACK_REDIRECT_URI", None)
        install_path = install_path or os.environ.get(
            "SLACK_LAMBDA_PATH", "/slack/install"
        )
        redirect_uri_path = redirect_uri_path or os.environ.get(
            "SLACK_LAMBDA_PATH", "/slack/oauth_redirect"
        )

        self.oauth_state_store = AmazonS3OAuthStateStore(
            logger=self.logger,
            s3_client=self.s3_client,
            bucket_name=oauth_state_bucket_name,
            expiration_seconds=oauth_state_expiration_seconds,
        )
        self.installation_store = AmazonS3InstallationStore(
            logger=self.logger,
            s3_client=self.s3_client,
            bucket_name=installation_bucket_name,
            client_id=client_id,
        )
        self.oauth_state_cookie_name = oauth_state_cookie_name
        self.oauth_state_expiration_seconds = oauth_state_expiration_seconds

        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes.split(",") if scopes else None
        self.user_scopes = user_scopes.split(",") if user_scopes else None
        self.redirect_uri = redirect_uri

        self.install_path = install_path
        self.redirect_uri_path = redirect_uri_path
        self.success_url = success_url
        self.failure_url = failure_url

        self._init_internal_utils()

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
