from typing import Optional, List, Union, Dict

from slack_bolt.context.say.internals import _can_say
from slack_sdk import WebClient
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.web import SlackResponse


class Say:
    client: Optional[WebClient]
    channel: Optional[str]

    def __init__(
        self, client: Optional[WebClient], channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    def __call__(
        self,
        text: str = "",
        blocks: Optional[List[Union[Dict, Block]]] = None,
        attachments: Optional[List[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
    ) -> SlackResponse:
        if _can_say(self, channel):
            return self.client.chat_postMessage(
                channel=channel or self.channel,
                text=text,
                blocks=blocks,
                attachments=attachments,
            )
        else:
            raise ValueError("say without channel_id here is unsupported")
