from typing import Optional

from slack_sdk import WebClient


def create_web_client(token: Optional[str] = None) -> WebClient:
    # TODO: add bolt info to user-agent
    return WebClient(token=token)
