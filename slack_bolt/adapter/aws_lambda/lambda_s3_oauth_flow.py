import logging
from logging import Logger
from typing import Optional

import boto3

from slack_bolt.oauth import OAuthFlow
from slack_sdk import WebClient
from slack_sdk.oauth.installation_store.amazon_s3 import AmazonS3InstallationStore
from slack_sdk.oauth.state_store.amazon_s3 import AmazonS3OAuthStateStore

from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.util.utils import create_web_client


class LambdaS3OAuthFlow(OAuthFlow):
    def __init__(
        self,
        *,
        client: Optional[WebClient] = None,
        logger: Optional[Logger] = None,
        settings: OAuthSettings,
        oauth_state_bucket_name: Optional[str] = None,  # required
        installation_bucket_name: Optional[str] = None,  # required
    ):
        super(OAuthFlow, self).__init__(
            client=client, logger=logger, settings=settings,
        )

        self.s3_client = boto3.client("s3")
        self.oauth_state_store = AmazonS3OAuthStateStore(
            logger=self.logger,
            s3_client=self.s3_client,
            bucket_name=oauth_state_bucket_name,
            expiration_seconds=self.settings.state_expiration_seconds,
        )
        self.installation_store = AmazonS3InstallationStore(
            logger=self.logger,
            s3_client=self.s3_client,
            bucket_name=installation_bucket_name,
            client_id=self.settings.client_id,
        )

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
