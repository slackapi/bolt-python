from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_chat_stream import AsyncChatStream


class AsyncSayStream:
    client: AsyncWebClient
    channel: Optional[str]
    recipient_team_id: Optional[str]
    recipient_user_id: Optional[str]
    thread_ts: Optional[str]

    def __init__(
        self,
        *,
        client: AsyncWebClient,
        channel: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        thread_ts: Optional[str] = None,
    ):
        self.client = client
        self.channel = channel
        self.recipient_team_id = recipient_team_id
        self.recipient_user_id = recipient_user_id
        self.thread_ts = thread_ts

    async def __call__(
        self,
        *,
        buffer_size: Optional[int] = None,
        channel: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        thread_ts: Optional[str] = None,
        **kwargs,
    ) -> AsyncChatStream:
        """Starts a new chat stream with context."""
        channel = channel or self.channel
        thread_ts = thread_ts or self.thread_ts
        if channel is None:
            raise ValueError("say_stream without channel here is unsupported")
        if thread_ts is None:
            raise ValueError("say_stream without thread_ts here is unsupported")

        if buffer_size is not None:
            return await self.client.chat_stream(
                buffer_size=buffer_size,
                channel=channel,
                recipient_team_id=recipient_team_id or self.recipient_team_id,
                recipient_user_id=recipient_user_id or self.recipient_user_id,
                thread_ts=thread_ts,
                **kwargs,
            )
        return await self.client.chat_stream(
            channel=channel,
            recipient_team_id=recipient_team_id or self.recipient_team_id,
            recipient_user_id=recipient_user_id or self.recipient_user_id,
            thread_ts=thread_ts,
            **kwargs,
        )
