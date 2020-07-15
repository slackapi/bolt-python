import time
from logging import Logger
from uuid import uuid4

from botocore.client import BaseClient

from .oauth_state_store import OAuthStateStore


class AmazonS3OAuthStateStore(OAuthStateStore):

    def __init__(
        self,
        *,
        logger: Logger,
        s3_client: BaseClient,
        bucket_name: str,
        expiration_seconds: int = 10 * 60,  # 10 minutes after creation
    ):
        self.logger = logger
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.expiration_seconds = expiration_seconds

    def issue(self) -> str:
        state = uuid4()
        response = self.s3_client.put_object(
            Bucket=self.bucket_name,
            Body=str(time.time()),
            Key=str(state),
        )
        self.logger.debug(f"S3 put_object response: {response}")
        return state

    def consume(self, state: str) -> bool:
        try:
            fetch_response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=state,
            )
            self.logger.debug(f"S3 get_object response: {fetch_response}")
            body = fetch_response["Body"].read().decode("utf-8")
            created = float(body)
            expiration = created + self.expiration_seconds
            still_valid: bool = time.time() < expiration

            deletion_response = self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=state,
            )
            self.logger.debug(f"S3 delete_object response: {deletion_response}")
            return still_valid
        except Exception as e:
            message = f"Failed to find any persistent data for state: {state} - {e}"
            self.logger.warning(message)
            return False
