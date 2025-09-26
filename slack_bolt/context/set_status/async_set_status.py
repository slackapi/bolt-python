from typing import List, Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncSetStatus:
    client: AsyncWebClient
    channel_id: str
    thread_ts: str

    def __init__(
        self,
        client: AsyncWebClient,
        channel_id: str,
        thread_ts: str,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts

    async def __call__(
        self,
        status: str,
        loading_messages: Optional[List[str]] = None,
        **kwargs,
    ) -> AsyncSlackResponse:
        return await self.client.assistant_threads_setStatus(
            channel_id=self.channel_id,
            thread_ts=self.thread_ts,
            status=status,
            loading_messages=loading_messages,
            **kwargs,
        )
