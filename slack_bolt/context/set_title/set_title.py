from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class SetTitle:
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

    def __call__(self, title: str) -> SlackResponse:
        return self.client.assistant_threads_setTitle(
            title=title,
            channel_id=self.channel_id,
            thread_ts=self.thread_ts,
        )
