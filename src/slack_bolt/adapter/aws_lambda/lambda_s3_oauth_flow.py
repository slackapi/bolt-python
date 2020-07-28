import os
from logging import Logger
from typing import Optional

import boto3

from slack_bolt.oauth.oauth_flow import OAuthFlow
from slack_sdk import WebClient
from slack_sdk.installation_store.amazon_s3_installation_store import AmazonS3InstallationStore
from slack_sdk.oauth_state_store.amazon_s3_oauth_state_store import AmazonS3OAuthStateStore


class LambdaS3OAuthFlow(OAuthFlow):

    def __init__(
        self,
        *,

        oauth_state_bucket_name: str = os.environ["SLACK_STATE_S3_BUCKET_NAME"],
        installation_bucket_name: str = os.environ["SLACK_INSTALLATION_S3_BUCKET_NAME"],
        oauth_state_cookie_name: str = "slack-app-oauth-state",
        oauth_state_expiration_seconds: int = 60 * 10,  # 10 minutes

        client_id: str = os.environ["SLACK_CLIENT_ID"],
        client_secret: str = os.environ["SLACK_CLIENT_SECRET"],
        scopes: Optional[str] = os.environ.get("SLACK_SCOPES", None),
        user_scopes: Optional[str] = os.environ.get("SLACK_USER_SCOPES", None),
        redirect_uri: Optional[str] = os.environ.get("SLACK_REDIRECT_URI", None),

        install_path: str = os.environ["SLACK_LAMBDA_PATH"],
        redirect_uri_path: str = os.environ["SLACK_LAMBDA_PATH"],

        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
    ):
        self.client: Optional[WebClient] = None
        self.logger: Optional[Logger] = None

        self.s3_client = boto3.client("s3")
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
