from typing import Optional

from slack_sdk import WebClient

from slack_bolt.version import __version__ as bolt_version


def create_web_client(token: Optional[str] = None) -> WebClient:
    return WebClient(token=token, user_agent_prefix=f"Bolt/{bolt_version}",)
