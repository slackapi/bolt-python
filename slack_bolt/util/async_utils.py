from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient


def create_async_web_client(token: Optional[str] = None) -> AsyncWebClient:
    # TODO: add bolt info to user-agent
    return AsyncWebClient(token=token)
