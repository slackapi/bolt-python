import warnings
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.web.chat_stream import ChatStream

from slack_bolt.warning import ExperimentalWarning


class SayStream:
    client: WebClient
    channel_id: Optional[str]
    thread_ts: Optional[str]
    team_id: Optional[str]
    user_id: Optional[str]

    def __init__(
        self,
        *,
        client: WebClient,
        channel_id: Optional[str] = None,
        thread_ts: Optional[str] = None,
        team_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts
        self.team_id = team_id
        self.user_id = user_id

    def __call__(
        self,
        *,
        buffer_size: Optional[int] = None,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
        **kwargs,
    ) -> ChatStream:
        warnings.warn(
            "say_stream is experimental and may change in future versions.",
            category=ExperimentalWarning,
            stacklevel=2,
        )

        channel = channel or self.channel_id
        thread_ts = thread_ts or self.thread_ts
        if channel is None:
            raise ValueError("say_stream without channel here is unsupported")
        if thread_ts is None:
            raise ValueError("say_stream without thread_ts here is unsupported")

        if buffer_size:
            return self.client.chat_stream(
                buffer_size=buffer_size,
                channel=channel,
                thread_ts=thread_ts,
                recipient_team_id=recipient_team_id or self.team_id,
                recipient_user_id=recipient_user_id or self.user_id,
                **kwargs,
            )

        return self.client.chat_stream(
            channel=channel,
            thread_ts=thread_ts,
            recipient_team_id=recipient_team_id or self.team_id,
            recipient_user_id=recipient_user_id or self.user_id,
            **kwargs,
        )
