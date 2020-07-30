from typing import Optional, List, Union, Dict

from slack_sdk.models.attachments import Attachment
from slack_sdk.models.block_kit import Block
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncSay():
    def __init__(
        self,
        client: Optional[AsyncWebClient],
        channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    async def __call__(
        self,
        text: Optional[str] = None,
        blocks: Optional[List[Union[Dict, Block]]] = None,
        attachments: Optional[List[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
    ) -> AsyncSlackResponse:
        if self.client is not None \
            and (channel or self.channel):
            return await self.client.chat_postMessage(
                channel=channel or self.channel,
                text=text,
                blocks=blocks,
                attachments=attachments,
            )
        else:
            raise ValueError("say without channel_id here is unsupported")
