from typing import Optional, List, Union, Dict

from slack_bolt.context.say.internals import _can_say
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncSay:
    client: Optional[AsyncWebClient]
    channel: Optional[str]

    def __init__(
        self, client: Optional[AsyncWebClient], channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    async def __call__(
        self,
        text: str = "",
        blocks: Optional[List[Union[Dict, Block]]] = None,
        attachments: Optional[List[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
    ) -> AsyncSlackResponse:
        if _can_say(self, channel):
            return await self.client.chat_postMessage(
                channel=channel or self.channel,
                text=text,
                blocks=blocks,
                attachments=attachments,
            )
        else:
            raise ValueError("say without channel_id here is unsupported")
