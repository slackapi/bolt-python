from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_chat_stream import AsyncChatStream


class AsyncSayStream:
    client: AsyncWebClient
    channel_id: Optional[str]
    thread_ts: Optional[str]
    team_id: Optional[str]
    user_id: Optional[str]

    def __init__(
        self,
        client: AsyncWebClient,
        channel_id: Optional[str],
        thread_ts: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str],
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts
        self.team_id = team_id
        self.user_id = user_id

    async def __call__(
        self,
        *,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        **kwargs,
    ) -> AsyncChatStream:
        provided = [arg for arg in (channel, thread_ts, recipient_team_id, recipient_user_id) if arg is not None]
        if provided and len(provided) < 4:
            raise ValueError(
                "Either provide all of channel, thread_ts, recipient_team_id, and recipient_user_id, or none of them"
            )
        channel = channel or self.channel_id
        thread_ts = thread_ts or self.thread_ts
        if channel is None:
            raise ValueError("say_stream is unsupported here as there is no channel_id")
        if thread_ts is None:
            raise ValueError("say_stream is unsupported here as there is no thread_ts")

        return await self.client.chat_stream(
            channel=channel,
            thread_ts=thread_ts,
            recipient_team_id=recipient_team_id or self.team_id,
            recipient_user_id=recipient_user_id or self.user_id,
            **kwargs,
        )
