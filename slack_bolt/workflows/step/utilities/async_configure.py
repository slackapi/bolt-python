from typing import Optional, Union, Sequence

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.models.blocks import Block


class AsyncConfigure:
    def __init__(self, *, callback_id: str, client: AsyncWebClient, body: dict):
        self.callback_id = callback_id
        self.client = client
        self.body = body

    async def __call__(
        self,
        *,
        blocks: Optional[Sequence[Union[dict, Block]]] = None,
    ) -> None:
        await self.client.views_open(
            trigger_id=self.body["trigger_id"],
            view={
                "type": "workflow_step",
                "callback_id": self.callback_id,
                "blocks": blocks,
            },
        )
