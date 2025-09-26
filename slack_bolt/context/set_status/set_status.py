from typing import List, Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class SetStatus:
    client: WebClient
    channel_id: str
    thread_ts: str

    def __init__(
        self,
        client: WebClient,
        channel_id: str,
        thread_ts: str,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts

    def __call__(
        self,
        status: str,
        loading_messages: Optional[List[str]] = None,
        **kwargs,
    ) -> SlackResponse:
        return self.client.assistant_threads_setStatus(
            channel_id=self.channel_id,
            thread_ts=self.thread_ts,
            status=status,
            loading_messages=loading_messages,
            **kwargs,
        )
