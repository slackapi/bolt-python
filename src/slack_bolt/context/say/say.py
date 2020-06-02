from typing import Optional, List

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class Say():
    def __init__(
        self,
        client: Optional[WebClient],
        channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    def __call__(self, text: str = None, blocks: List[dict] = [], channel: str = None) -> SlackResponse:
        if self.client is not None \
            and (channel or self.channel):
            return self.client.chat_postMessage(
                channel=channel or self.channel,
                text=text,
                blocks=blocks
            )
        else:
            raise ValueError("say without channel_id here is unsupported")
