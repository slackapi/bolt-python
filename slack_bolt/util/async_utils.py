from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.version import __version__ as bolt_version


def create_async_web_client(token: Optional[str] = None) -> AsyncWebClient:
    return AsyncWebClient(
        token=token,
        user_agent_prefix=f"Bolt-Async/{bolt_version}",
    )
