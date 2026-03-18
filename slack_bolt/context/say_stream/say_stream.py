import warnings
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.web.chat_stream import ChatStream

from slack_bolt.warning import ExperimentalWarning


class SayStream:
    client: WebClient
    channel: Optional[str]
    thread_ts: Optional[str]
    recipient_team_id: Optional[str]
    recipient_user_id: Optional[str]

    def __init__(
        self,
        *,
        client: WebClient,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        recipient_team_id: Optional[str] = None,
        recipient_user_id: Optional[str] = None,
    ):
        self.client = client
        self.channel = channel
        self.thread_ts = thread_ts
        self.recipient_team_id = recipient_team_id
        self.recipient_user_id = recipient_user_id

    def __call__(
        self,
        *,
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

        channel = channel or self.channel
        thread_ts = thread_ts or self.thread_ts
        if channel is None:
            raise ValueError("say_stream without channel here is unsupported")
        if thread_ts is None:
            raise ValueError("say_stream without thread_ts here is unsupported")

        return self.client.chat_stream(
            channel=channel,
            thread_ts=thread_ts,
            recipient_team_id=recipient_team_id or self.recipient_team_id,
            recipient_user_id=recipient_user_id or self.recipient_user_id,
            **kwargs,
        )
